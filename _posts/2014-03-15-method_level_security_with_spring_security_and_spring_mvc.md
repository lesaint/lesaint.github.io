---
layout: post
title: Implementing method-level security with Spring Security and Spring MVC
tags: SpringMVC SpringSecurity AOP
categories: articles
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/03/15/method_level_security_with_spring_security_and_spring_mvc.html
---

Using Spring Security with Spring MVC to provide method level security on Controller classes can be trooblesome : using CGLIB-based proxies might be mandatory and you might need to tweak your code to fit Spring.

When setting up exactly just that on a project, I ran into a series of problem and got a finer understanding on how Spring Security implements Method Security.


# How to enable Method Security

As stated by the [documentation](http://docs.spring.io/spring-security/site/docs/3.1.x/reference/el-access.html#d0e5600), enabling Method level security with Spring Security is as simple as added a `global-method-security` tag in your configuration.

It's super easy and it works. You can even choose which annotation set you want to use with the appropriate attributes: 

* `secured-annotations="enabled"` for `@Secured`
* `jsr250-annotations="enabled"` for `@RolesAllowed`
* `pre-post-annotations="enabled"` for `@PreAuthorize`, `@PostAuthorize`, ...
* `metadata-source-ref="extraMethodSecurityMetadataSource"` to use your own annotations
	- more on that in another article

# Pitfalls when using Method Security on Spring MVC controllers

But in fact, it's not that easy, especially with Spring MVC controllers.

## The position of `global-method-security` matters

The first problem I encountered when adding `@Secured` annotations on my Controller classes was that it simply didn't work. Spring would not enforce the required role(s), not even applying any control. My Controller classes didn't seem to be secured at all.

In fact, they weren't.

After some googling, I found out that the position of the `global-method-security` tag in the configuration files is **very** important. Only the beans in the current context seems to be "secured" (in fact proxied, more on that below).

As most people using Spring MVC, I had two Spring Application Contexts (AP) : one for the application and one for the DispatchServlet which inherits from the application context.

In this conditions, having the `global-method-security` tag in the application AP would ignore the Controller class declared/scanned in the DispatchServlet AP.

The solution is as simple as it seems : put the `global-method-security` tag in the DispatchServlet AP.

But if like me you have a Spring AP config file dedicated to Spring Security configuration, it will be part of the application's AP. And you will be sad to have to put just that one tag in another config file.

I found out I couldn't make the Spring Security config part of the DispatchServlet's AP.
The DispatchServlet AP's would fail to start because no FilterChain bean existed when instanciating the `org.springframework.web.filter.DelegatingFilterProxy` declared in the web.xml.

So I put the `global-method-security` tag in the DispatcherServlet AP and was off to meet to the next problems :)

## Having classes annoted with @Controller

To implement Method Security, Spring Security uses Spring AOP to create proxies of the annoted controllers. Proxies implements the security checks and it they are ok, call the user's class.
By default, Spring will use JDK dynamic proxies to create a proxy object with the same methods as your class but which will not be an instance of your class.

This will more often that not cause errors at some point. The one I encountered is the following one where Spring MVC can not invoke the handler method :

```
java.lang.IllegalArgumentException: object is not an instance of declaring class
sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
java.lang.reflect.Method.invoke(Method.java:606)
org.springframework.web.method.support.InvocableHandlerMethod.invoke(InvocableHandlerMethod.java:219)
org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:132)
org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:104)
org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandleMethod(RequestMappingHandlerAdapter.java:745)
org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:686)
org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:80)
org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:925)
org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:856)
org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:936)
org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:827)
javax.servlet.http.HttpServlet.service(HttpServlet.java:621)
org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:812)
javax.servlet.http.HttpServlet.service(HttpServlet.java:728)
org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:88)
org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:330)
org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:118)
org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:84)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:113)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:54)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:183)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:105)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:87)
org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:342)
org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:192)
org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:160)
org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:343)
org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:260)
org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107)
```

What happens under the hood it that Spring MVC tries and fails to invoke the method annoted with `@RequestMapping` via refection. The `Method` instance it created when parsing controllers is based on the type of the concrete class of our controller.
As the JDK proxy object is **not** an instance of the Controller class, we get a `IllegalArgumentException`.

A fast and efficient workaround this is to make Spring AOP create another type of proxy by adding `proxy-target-class="true"` to the `global-method-security` tag.
This will tell Spring to use CGLIB-based subclass proxies instead of JDK dynamic proxies. Such proxies are actual instances of the proxied classes. That fixes our problem.

## Having controller classes without default constructor

Happiness won't last though, if you have controllers which does not declare a default constructor. 

If like me you favour constructor injection over property injection then your controller classes do not define a default constructor (well, they could, but not mine).
So you're in for more trouble because CGLIB-based proxies require a default constructor to be created (see [http://docs.spring.io/spring/docs/3.1.x/spring-framework-reference/html/aop.html#aop-proxying](http://docs.spring.io/spring/docs/3.1.x/spring-framework-reference/html/aop.html#aop-proxying) for details).

The DispatchServlet AP fails to start with an error such as the following :

```
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'managerController' defined in file [********************************/ManagerController.class]: Initialization of bean failed; nested exception is org.springframework.aop.framework.AopConfigException: Could not generate CGLIB subclass of class [class **********************.ManagerController]: Common causes of this problem include using a final class or a non-visible class; nested exception is java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:529)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:458)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:295)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:223)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:292)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:194)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:628)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:932)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:479)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:651)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:599)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:665)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:518)
	at **********************.initWebApplicationContext(**********:**)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:459)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:136)
	at javax.servlet.GenericServlet.init(GenericServlet.java:160)
	at org.apache.catalina.core.StandardWrapper.initServlet(StandardWrapper.java:1280)
	at org.apache.catalina.core.StandardWrapper.loadServlet(StandardWrapper.java:1193)
	at org.apache.catalina.core.StandardWrapper.load(StandardWrapper.java:1088)
	at org.apache.catalina.core.StandardContext.loadOnStartup(StandardContext.java:5033)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5317)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:150)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1559)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1549)
	at java.util.concurrent.FutureTask.run(FutureTask.java:262)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1145)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:615)
	at java.lang.Thread.run(Thread.java:744)
Caused by: org.springframework.aop.framework.AopConfigException: Could not generate CGLIB subclass of class [class ****************.ManagerController]: Common causes of this problem include using a final class or a non-visible class; nested exception is java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.aop.framework.CglibAopProxy.getProxy(CglibAopProxy.java:217)
	at org.springframework.aop.framework.ProxyFactory.getProxy(ProxyFactory.java:111)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.createProxy(AbstractAutoProxyCreator.java:477)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.wrapIfNecessary(AbstractAutoProxyCreator.java:362)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.postProcessAfterInitialization(AbstractAutoProxyCreator.java:322)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyBeanPostProcessorsAfterInitialization(AbstractAutowireCapableBeanFactory.java:409)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1488)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:521)
	... 28 common frames omitted
Caused by: java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.cglib.proxy.Enhancer.emitConstructors(Enhancer.java:721)
	at org.springframework.cglib.proxy.Enhancer.generateClass(Enhancer.java:499)
	at org.springframework.cglib.transform.TransformingClassGenerator.generateClass(TransformingClassGenerator.java:33)
	at org.springframework.cglib.core.DefaultGeneratorStrategy.generate(DefaultGeneratorStrategy.java:25)
	at org.springframework.cglib.core.AbstractClassGenerator.create(AbstractClassGenerator.java:216)
	at org.springframework.cglib.proxy.Enhancer.createHelper(Enhancer.java:377)
	at org.springframework.cglib.proxy.Enhancer.create(Enhancer.java:285)
	at org.springframework.aop.framework.CglibAopProxy.getProxy(CglibAopProxy.java:205)
	... 35 common frames omitted
```

To fix this error, just add a default constructor to your bean :

```java
@Controller
public class ManagerController {

  private final SomeService someService;

  // default constructor for CGLIB proxying
  // default constructor is called first and then public constructor is called with autowired dependencies
  // required to use the @Secured annotation on methods of this class
  public ManagerController() {
    this(null, null);
  }

  @Autowired
  public ManagerController(SomeService someService) {
    this.someService = someService;
  }

  @RequestMapping("/all")
  @Secured("ROLE_VIEW_MANAGERS")
  public String list() {
  	return "viewname";
  }
}
```

### Using a private default constructor

With Spring 3.2.4, the default constructor used by CGLIB-based proxies does not need to be public, so we can use a private constructor. This will avoid poluting the exposed methods of your class, but it is not very elegant nor practical. 
In fact, it is very annoying to have to add private default constructor to every Controller class that will use the `@Secured` annotation and a non-default constructor.

With Spring 3.2.8, this is not possible anyway. The default constructor has to be public otherwise proxy creation fails with the following error:

```
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'managerController' defined in file [****************************************/ManagerController.class]: Initialization of bean failed; nested exception is org.springframework.aop.framework.AopConfigException: Could not generate CGLIB subclass of class [class **********************.ManagerController]: Common causes of this problem include using a final class or a non-visible class; nested exception is java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:529)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:458)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:296)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:223)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:293)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:194)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:628)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:932)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:479)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:651)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:602)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:665)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:521)
	at **********************.initWebApplicationContext(**************:**)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:462)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:136)
	at javax.servlet.GenericServlet.init(GenericServlet.java:160)
	at org.apache.catalina.core.StandardWrapper.initServlet(StandardWrapper.java:1280)
	at org.apache.catalina.core.StandardWrapper.loadServlet(StandardWrapper.java:1193)
	at org.apache.catalina.core.StandardWrapper.load(StandardWrapper.java:1088)
	at org.apache.catalina.core.StandardContext.loadOnStartup(StandardContext.java:5033)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5317)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:150)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1559)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1549)
	at java.util.concurrent.FutureTask.run(FutureTask.java:262)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1145)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:615)
	at java.lang.Thread.run(Thread.java:744)
Caused by: org.springframework.aop.framework.AopConfigException: Could not generate CGLIB subclass of class [class ******************.ManagerController]: Common causes of this problem include using a final class or a non-visible class; nested exception is java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.aop.framework.CglibAopProxy.getProxy(CglibAopProxy.java:218)
	at org.springframework.aop.framework.ProxyFactory.getProxy(ProxyFactory.java:111)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.createProxy(AbstractAutoProxyCreator.java:477)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.wrapIfNecessary(AbstractAutoProxyCreator.java:362)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.postProcessAfterInitialization(AbstractAutoProxyCreator.java:322)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyBeanPostProcessorsAfterInitialization(AbstractAutowireCapableBeanFactory.java:409)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1518)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:521)
	... 28 common frames omitted
Caused by: java.lang.IllegalArgumentException: Superclass has no null constructors but no arguments were given
	at org.springframework.cglib.proxy.Enhancer.emitConstructors(Enhancer.java:721)
	at org.springframework.cglib.proxy.Enhancer.generateClass(Enhancer.java:499)
	at org.springframework.cglib.transform.TransformingClassGenerator.generateClass(TransformingClassGenerator.java:33)
	at org.springframework.cglib.core.DefaultGeneratorStrategy.generate(DefaultGeneratorStrategy.java:25)
	at org.springframework.cglib.core.AbstractClassGenerator.create(AbstractClassGenerator.java:216)
	at org.springframework.cglib.proxy.Enhancer.createHelper(Enhancer.java:377)
	at org.springframework.cglib.proxy.Enhancer.create(Enhancer.java:285)
	at org.springframework.aop.framework.CglibAopProxy.getProxy(CglibAopProxy.java:206)
	... 35 common frames omitted
```

### Using Controller interfaces

Theoretically, a way around the ugly default constructor is to add Spring MVC and Security annotations on an interface instead of a concrete class.

This way, we do not need to use CGLIB-based proxies and can stick to JDK proxies.

```java
@Controller
public interface ManagerController {

  @RequestMapping("/all")
  @Secured("ROLE_VIEW_MANAGERS")
  String list();
}
```

```java
@Component
public class ManagerControllerImpl implements ManagerController {

  private final SomeService someService;

  @Autowired
  public ManagerController(SomeService someService) {
    this.someService = someService;
  }

  @Override
  public String list() {
  	return "viewname";
  }
}
```


> Please note that the `@Controller` annotation has been moved to the interface as well as `@RequestMapping` and `@Control` annotations.
Unfortunatly, **this doesn't work with Spring MVC**.

In this case as well in the one where we started struggling with Spring-AOP in the first place, we get the `object is not an instance of declaring class` exception from the `Having classes annoted with @Controller` part.

I'm wonder if this is a bug or at least if it could be improved...

# Conclusion

For the time beeing I will stick to the CGLIB-enabled proxies with the default controller solution.

But I will try and see later if AspectJ couldn't be used to weave beans at compile time and remove the use of proxy completly.

# Some references

While working and googling on this issue, I found this interrested comment on Stackoverflow which discusses the reasons to use Spring-AOP with controller when many ways to implements cross cutting concerns exist:
[http://stackoverflow.com/a/12045331](http://stackoverflow.com/a/12045331).

I wrote an article on using one of theses other way in [TODO article on generatic pagination solution with Spring MVC]().

Also, on the subject of comparing JDK proxies and CGLIB-based proxies, this article points that @Transaction annotation does not work with JDK proxies:
[Spring annotation on interface or class implementing the interface??](http://kim.saabye-pedersen.org/2013/05/spring-annotation-on-interface-or-class.html)

References in Spring documentation 

* to the Spring-AOP vs Controller in the information note `Using @RequestMapping On Interface Methods` [here](http://docs.spring.io/spring/docs/3.1.x/spring-framework-reference/html/mvc.html#mvc-ann-requestmapping)
* to enable Method Security [http://docs.spring.io/spring-security/site/docs/3.1.x/reference/el-access.html#d0e5600](http://docs.spring.io/spring-security/site/docs/3.1.x/reference/el-access.html#d0e5600)

Various articles on the use of `proxy-target-class="true"` on the `global-method-security` tag:

* [http://stackoverflow.com/questions/10726478/spring-securitymvc-annotations-illegal-argument-exception](http://stackoverflow.com/questions/10726478/spring-securitymvc-annotations-illegal-argument-exception)
* [http://stackoverflow.com/questions/18663475/spring-security-global-method-security-does-not-work](http://stackoverflow.com/questions/18663475/spring-security-global-method-security-does-not-work)
	- This discusses how to work around proxies completly by using AspectJ weaving at compile time
	- This is mandatory when using controller not managed as Spring beans and could be a workaround the ugly default constructor discussed above

Article on the importance of the position of the `global-method-security` tag in your Spring Config :
[http://stackoverflow.com/questions/517527/spring-not-enforcing-method-security-annotations](http://stackoverflow.com/questions/517527/spring-not-enforcing-method-security-annotations)
