Title: Using a TestRule to initialize Mockito Mocks in a JUnit test
Tags: Java, JUnit, Mockito, Spring MVC

Using Mockito annotations in JUnit tests is very convenient.

To make it even easier, initialisation can be made automatic by using a Runner (with annotation `@RunWith(MockitoJUnitRunner.class`) that will call `MockitoAnnotations.initMocks(Object)` for us.

The problem is : the runner is executed after the class is initialized by constructor (obviously), making it impossible, for example, to have references to mocks or injected objects in rules.


# Using a TestRule to initialize the class

The solution around this is pretty simple, but it is not provided by Mockito as far as I could see : use a TestRule to initialize the class instead of a Runner.

Here is the code of the TestRule (very simple, indeed) :

```java
package fr.phan.testfr.phan.webapp.controller.test;

import org.junit.rules.TestRule;
import org.junit.runner.Description;
import org.junit.runners.model.Statement;
import org.mockito.MockitoAnnotations;

public class MockitoAnnotationsRule implements TestRule {
  public MockitoAnnotationsRule(Object test) {
    MockitoAnnotations.initMocks(test);
  }

  @Override
  public Statement apply(Statement base, Description description) {
    return base;
  }
}
```

This class takes the Unit test as a contructor argument and simply calls `MockitoAnnotations.initMocks()` on it.

# Usage

This TestRule is intended to be used as a public, non static property in a JUnit test, annoted with `@Rule`.
The only constraint is that the property must be placed in the code before any other rule or object instanced during the creation of the test Object which uses a property annoted with either `@Mock` or `@InjectMocks`.

Sample usage in unit test for a Spring MVC controller :

```java
package fr.phan.webapp.controller;

import fr.phan.webapp.controller.test.MyMockMvc;
import fr.phan.webapp.controller.test.MockitoAnnotationsRule;
import fr.phan.webapp.controller.view.ExtranetView;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class MyControllerTest {

  @Mock
  private PeanutService peanutService;
  @InjectMocks
  private MyController controller;

  @Rule
  public MockitoAnnotationsRule mockitoAnnotationsRule = new MockitoAnnotationsRule(this);
  @Rule
  /** MyMockMvc decorates a MockMvc instance and factorizes initialization code generic to the whole webapp */
  public MyMockMvc mockMvc = new MyMockMvc(controller);

  @Test
  public void get_should_return_ok() throws Exception {
    mockMvc.perform(get("/toto"))
      .andExpect(status().isOk());
  }

}
```

# Comments

## Comparison of using a TestRule against using a Runner :

* Pros
    - benefits of the TestRule paradigm over the Runner paradigm
        + one can use any number of TestRule but only one Runner in a Test
        + one can decide to execute a Rule before another one by just ordering the properties
    - code is easily shared and one can use mock and injected objects in other TestRule or objects created during the test Object's initialisation
* Cons
    - quite more verbose than adding `@RunWith(MockitoJUnitRunner.class)`

## Is it really a TestRule ?

Some might say that `MockitoAnnotationsRule` beeing a `TestRule` is not relevant since it provides no useful implementation for the `apply` defined by the `TestRule` interface.

Very good point. I could even add that it probably adds (some minor) overhead to the statement execution since our `apply` method is called but does nothing.

But on the other hand, adding the `@Rule` annotation on our `MockitoAnnotationsRule` property adds a great deal of readibility and defines clearly its purpose.

That's why I will stay with implementing `TestRule`.
