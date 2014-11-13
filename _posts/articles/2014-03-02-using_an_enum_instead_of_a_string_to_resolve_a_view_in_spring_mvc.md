---
layout: post
title: Using enum instead of String to resolve views in Spring MVC
tags:
 - Spring MVC
categories: articles
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/03/02/using_an_enum_instead_of_a_string_to_resolve_a_view_in_spring_mvc.html
comments: true
---

The project I'm currently working on uses Spring MVC. This framework is nice, mature and efficient.

But we are using `String` as return type of our `@RequestMapping` methods (as most people probably do) and I don't like that very much.

I want to use and enum instead. I want `@RequestMapping` methods to return a enum constant which will be automatically resolved to a view the same way a `String` is resolved to a view.


* Table of Contents
{:toc}

# Using an enum is good

Using `String` as return value of controller methods to represent view name is bad:
* bad for maintenance
* bad for refactoring
* obviously not type-safe
* adds magic numbers to your code

Using an enum has many positive side effects :
* view names are all in the same place
* if it easy to tell which view is used or not with any IDE
* refactoring is much easier 

# How to add support for an enum return type in Spring MVC

## create a enum with a String property

The string property will hold the String value `@RequestMapping` methods used to return.

{% highlight java %}
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
{% endhighlight %}

## create a `HandlerMethodReturnValueHandler`

If we make our `@RequestMapping` methods return a value of `MyView` and run our website, Spring will simply add the value to the model and won't resolve a view and fail.

To fix, that, we need to provide with an extra `HandlerMethodReturnValueHandler` which will "convert" our enum to its String property.
To be more accurate, we need to set the `viewName` in the `ModelAndViewContainer` of the current request.

{% highlight java %}
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

{% endhighlight %}

(inspiration: Spring's `org.springframework.web.servlet.mvc.method.annotation.ViewNameMethodReturnValueHandler` class)

## add our `HandlerMethodReturnValueHandler` to the Spring MVC's servlet context

After some investigation on the web, I found that the easiest way of adding an extra `HandlerMethodReturnValueHandler` to the Spring MVC servlet context is to use programmatic configuration.

I found a like to this bug report [https://jira.springsource.org/browse/SPR-8648](https://jira.springsource.org/browse/SPR-8648) which has a useful comment pointing to the source code of Spring's Greenhouse Reference Application.

Since I already had some XML-based configuration in place, I created a Configuration class which referes to my XML config and therefor is pretty simple :

{% highlight java %}
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
{% endhighlight %}

What's important here :

* `@Configuration` annotation is obviously mandatory
* `@EnableWebMVC` annotation is also required so that the `WebMvcConfigurerAdapter` interface we extends is taken into account
* the `WebMvcConfigurerAdapter` provides empty implementations of the `WebMvcConfigurer` interface methods
  - we can then override only those we need, in our case : `addReturnValueHandlers` 
* the `@ImportResource` is here to load our legacy XML configuration
  - existing XML configuration should be usable as is with one very important retriction :
    + the `<annotation-driven/>` tag of the MVC XML namespace should be remove as the `@EnableWebMVC` annotation is its exact programmatic equivalent.
      Not doing so will most likely make Spring fail to load your context, but the error you would get will moke likely not obviously point to the `<annotation-driven/>` tag.

# Conclusion

This solution is working like a charm and I like it very much. Spring easy extensibility was a real pleasure to discover.

I wonder if this solution could be made generic and bundle into Spring MVC...
