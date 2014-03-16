---
layout: post
title: Using enum instead of String to resolve view
---

On the current project I'm working on, we are using Spring MVC. This framework is nice, mature and efficient.

But we are currently using String as return type of our `@RequestMapping` methods (as most people probably do) and I don't like that very much. We end up having magic number Strings in the code or (better but not great) constants in controllers.

I would rather have all the name of the views in a single place, an enum for exemple. Better, I would like `@RequestMapping` methods to return a enum constant representing the view to forward to.

Spring MVC supports a lot of return types out-of-the-box but not enums. Here is how to extends Spring MVC to do it.


## create a enum with a String property

The string property will hold the String value `@RequestMapping` methods used to return.

```java
public enum MyView {
  HOME("home"),
  LOGIN("login"),
  CUSTOMER_LIST("customer/list")  ;

  @Nonnull
  private final String logicalViewName;

  private ExtranetView(@Nonnull String logicalViewName) {
    this.logicalViewName = Preconditions.checkNotNull(logicalViewName);
  }

  @Nonnull
  public String getLogicalViewName() {
    return logicalViewName;
  }
}
```

## create a `HandlerMethodReturnValueHandler`

If we make our `@RequestMapping` methods return a value of `MyView` and run our website, Spring will simply add the value to the model and won't resolve a view and fail.

To fix, that, we need to provide with an extra `HandlerMethodReturnValueHandler` which will "convert" our enum to its String property.
To be more accurate, we need to set the `viewName` in the `ModelAndViewContainer` of the current request.

```java
public class MyViewEnumModelAndViewResolver implements HandlerMethodReturnValueHandler {

  @Override
  public boolean supportsReturnType(MethodParameter returnType) {
    return MyView.class.isAssignableFrom(returnType.getParameterType());
  }

  @Override
  public void handleReturnValue(Object returnValue, MethodParameter returnType, ModelAndViewContainer mavContainer, NativeWebRequest webRequest) throws Exception {
    if (returnValue == null) {
      return;
    }
    if (returnValue instanceof MyView) {
      String viewName = ((MyView) returnValue).getLogicalViewName();
      mavContainer.setViewName(viewName);
    }
    else {
      // should not happen
      throw new UnsupportedOperationException("Unexpected return type: " +
        returnType.getParameterType().getName() + " in method: " + returnType.getMethod());
    }
  }
}

```

(inspiration: Spring's `org.springframework.web.servlet.mvc.method.annotation.ViewNameMethodReturnValueHandler` class)

## add our `HandlerMethodReturnValueHandler` to the Spring MVC's servlet context

After some investigation on the web, I found that the easiest way of adding an extra `HandlerMethodReturnValueHandler` to the Spring MVC servlet context is to use programmatic configuration.

I found a like to this bug report [https://jira.springsource.org/browse/SPR-8648](https://jira.springsource.org/browse/SPR-8648) which has a useful comment pointing to the source code of Spring's Greenhouse Reference Application.

Since I already had some XML-based configuration in place, I created a Configuration class which referes to my XML config and therefor is pretty simple :

```java
@Configuration
@EnableWebMvc
@ImportResource({
  "classpath:/META-INF/spring/my-dispatcher-servlet.xml",
})
public class MyMvcConfig extends WebMvcConfigurerAdapter {
  @Override
  public void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> returnValueHandlers) {
    returnValueHandlers.add(
      new MyViewEnumModelAndViewResolver()
    );
  }

}
```

What's important here :

* `@Configuration` annotation is obviously mandatory
* `@EnableWebMVC` annotation is also required so that the `WebMvcConfigurerAdapter` interface we extends is taken into account
* the `WebMvcConfigurerAdapter` provides empty implementations of the `WebMvcConfigurer` interface methods
  - we can then override only those we need, in our case : `addReturnValueHandlers` 
* the `@ImportResource` is here to load our legacy XML configuration
  - existing XML configuration should be usable as is with one very important retriction :
    + the `<annotation-driven/>` tag of the MVC XML namespace should be remove as the `@EnableWebMVC` annotation is its exact programmatic equivalent.
      Not doing so will most likely make Spring fail to load your context, but the error you would get will moke likely not obviously point to the `<annotation-driven/>` tag.
