---
layout: post
title: A SMTP server in Java for unit test
tags: java, junit, smtp, unit testing
---

If you ever had to write code that uses JavaMail to send emails, then you necessarily looked for a way of testing that code at some point.
If you didn't, its bad. Otherwise, you have been looking for a pure-Java implementation of a SMTP server.
The subject is old and googling will return several framework names accross multiple blog posts, forum questions, ... I recently add to do that research and here are my conclusions.

# Several products available

A little research on the web and you find name such as [dumbster](http://quintanasoft.com/dumbster/), [GreenMail](http://www.icegreen.com/greenmail/) or [wiser](http://code.google.com/p/subethasmtp/wiki/Wiser).

Comparing the frameworks has already been done, so I will just link to this [article](http://eokyere.blogspot.fr/2006/10/get-wiser-with-subethasmtp.html) and add my personnal points :
* Wiser is latest and most recently player in the area
* Wiser is meant for unit testing and is therefor fast and easy to use
* Greenmail has thread-safety issues in its 1.3 version and has a buggy way of handling senders/cc/bcc in its latest version (1.3.1b)
* Greenmail doesn't seem to be maintained since 2009
* Wiser doesn't seem to be maintained since 2012

# How to use Wiser

Add subethasmtp maven dependency to your project :

```xml
<dependency>
  <groupId>org.subethamail</groupId>
  <artifactId>subethasmtp</artifactId>
  <version>3.1.7</version>
  <scope>test</scope>
</dependency>
```

To Start the Wiser SMTP Server, just create a new instance, setup port and hostname, and start it :

```java
Wiser wiser = new Wiser();
wiser.setPort(25);
wiser.setHostname("localhost");
wiser.start();
```

You can then use JavaMail to send mail to the port and hostname you specified and then test received messages as follow :

```java
assertThat(wiser.getMessages()).hasSize(1);
MimeMessage message = wiser.getMessages().iterator().next().getMimeMessage();
assertThat(message.getSubject()).isEqualTo("Here is a sample subject !");
[...]
```

# Integrating Wiser with JUnit

I found very convenient when integrating Wiser into JUnit tests to use a Rule.
And also, when writing unit test, one has to been carreful about the port then want to use. It must either be unique to the maven module (assuming tests are not run in parallel) or unique to the test.
Either way, assuming it is known to the unit test, I came up with the following implementation :

```java
package fr.phan.test.rule;

import com.google.common.base.Preconditions;
import org.junit.rules.ExternalResource;
import org.junit.rules.TestRule;
import org.subethamail.smtp.TooMuchDataException;
import org.subethamail.smtp.server.SMTPServer;
import org.subethamail.wiser.Wiser;
import org.subethamail.wiser.WiserMessage;

import javax.annotation.Nonnull;
import javax.mail.MessagingException;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;
import java.util.List;


/**
 * SmtpServerRule - a TestRule wrapping a Wiser instance (a SMTP server in Java) started and stoped right before and after each test.
 * <br/>
 * SmtpServerRule exposes the same methods as the {@link Wiser} instance by delegating the implementation to the instance. These methods, however, can not be
 * used outside a JUnit statement (otherwise a {@link IllegalStateException} is raised).
 * <br/>
 * The {@link Wiser} instance can be directly retrieved but also only from inside a JUnit statement.
 *
 * @author Sébastien Lesaint
 */
public class SmtpServerRule extends ExternalResource implements TestRule {
  private final SmtpServerSupport SmtpServerSupport;
  private Wiser wiser;

  public SmtpServerRule(@Nonnull SmtpServerSupport SmtpServerSupport) {
    this.SmtpServerSupport = Preconditions.checkNotNull(SmtpServerSupport);
  }

  @Override
  protected void before() throws Throwable {
    this.wiser = new Wiser();
    this.wiser.setPort(SmtpServerSupport.getPort());
    this.wiser.setHostname(SmtpServerSupport.getHostname());
    this.wiser.start();
  }

  @Override
  protected void after() {
    this.wiser.stop();
  }

  /**
   * @return the inner {@link Wiser} instance
   * @throws IllegalStateException is method is not called from a JUnit statement
   */
  @Nonnull
  public Wiser getWiser() {
    checkState("getWiser()");
    return this.wiser;
  }

  /**
   * @return a {@link List} of {@link WiserMessage}
   * @throws IllegalStateException is method is not called from a JUnit statement
   * @see {@link Wiser#getMessages()}
   */
  @Nonnull
  public List<WiserMessage> getMessages() {
    checkState("getWiser()");
    return wiser.getMessages();
  }

  /**
   * @throws IllegalStateException is method is not called from a JUnit statement
   * @see {@link Wiser#getServer()}
   */
  @Nonnull
  public SMTPServer getServer() {
    checkState("getServer()");
    return wiser.getServer();
  }

  /**
   * @throws IllegalStateException is method is not called from a JUnit statement
   * @see {@link Wiser#accept(String, String)}
   */
  public boolean accept(String from, String recipient) {
    checkState("accept(String, String)");
    return wiser.accept(from, recipient);
  }

  /**
   * @throws IllegalStateException is method is not called from a JUnit statement
   * @see {@link Wiser#deliver(String, String, java.io.InputStream)}
   */
  public void deliver(String from, String recipient, InputStream data) throws TooMuchDataException, IOException {
    checkState("deliver(String, String, InputStream)");
    wiser.deliver(from, recipient, data);
  }

  /**
   * @throws IllegalStateException is method is not called from a JUnit statement
   * @see {@link Wiser#dumpMessages(java.io.PrintStream)}
   */
  public void dumpMessages(PrintStream out) throws MessagingException {
    checkState("dumpMessages(PrintStream)");
    wiser.dumpMessages(out);
  }

  private void checkState(String method) {
    Preconditions.checkState(this.wiser != null, "%s must not be called outside of a JUnit statement", method);
  }
}
```

And the `SmtpServerSupport` interface which will usually be implemented by the JUnit test :

```java
package fr.phan.test.rule;

import javax.annotation.Nonnull;

/**
 * SmtpServerSupport - Interface usually implemented by the JUnit test class.
 *
 * @author Sébastien Lesaint
 */
public interface SmtpServerSupport {
  /**
   * the SMTP port.
   */
  int getPort();

  /**
   * The hostname (for example 'localhost')
   *
   * @return a {@link String}
   */
  @Nonnull
  String getHostname();
}
```

## which port to use ?



# To go a little bit further

## class Rule
The current implementation of the Rule starts and stops the SMTP server around each test. It might be more efficient to implement a class Rule which starts/stops the server only one per class.
To do so, the only point to investigate is how to reset the status of the SMTP before each test, ie. clearing received messages. I haven't looked into that yet.

## random port
Another could feature would be to create the rule in a mode where the port would be chosen at random, the SMTP server started and if the start fails another port choosen and tried in loop for several times.
Combined with the class Rule feature, this feature would be extremely convenient to create tests which can be run in parallel inside the same maven module.
To do so, the only point to investigate is wheter `wiser.start()` fails immediatly if the port is not available.



