---
layout: post
title: Using advanced Spring MVC to implement Data pagination
tags: SpringMVC
image:
 feature: feature_image_green.png
---

This article will present how to use some advanced features of Spring MVC in order to add cross-webapp support for Data pagination.

The goal is that very little code will then be required to implement pagination in any `@RequestMapping` method.



* an implementation of `HandlerInterceptor`
* an implementation of `HandlerMethodArgumentResolver`
* several model objects
* a little bit of Spring MVC configuration to get all that together


# Quick definitions

## What is Pagination

Paginating data is about beeing able to display only parts of a long list of data (usually displayed as an HTML table) and being able
to navigate from one part to another. Parts of the list are refered to as `Pages`.

The User Interface (`UI`) usually informs the user of the total number of page and allows her to navigate from one page to another
(aka. `Pagination navigation`).

The total number of pages requires to know the total number of items in the list to be calculated.

`Pagination navigation` can take many forms, from the most basic 'previous page' - 'next page' links one can find on blogs to complexe
list of pages numbers at the bottom of HTML tables.
In all cases, `Pagination navigation` also requires to know the total number of items to be displayed.

## What is a Page

A `Page` is defined by two properties:

* an index, to know which part we are talking about
    - it's a positive integer
    - it starts at 1 because that how humans will identify the first page
* the current number of items per page
    - the content of the page can be totally different depending on the number of items per page
    - it's a positive integer also
    - it starts at 0, which means no-pagination-at-all or all-on-one-page since a page of 0 item does not make any sense

# What we want

When coding a `@RequestMapping` which must be pagination-aware, what the developer expects is:

1. being able to define a list of valid number(s) of items per page
    - this list of valid numbers could be also used to allow the user to change the number of items per page in the UI
    - there could very well be only one valid number of item per page. In such case, the user will not be able to change it
    - 
2. know which page is requested in the current request
    - developer doesn't want to deal with the retrieval of parameters from the HTTP request
    - nor does she want to validate those parameters
3. extra feature (but a must-have): when there is no explicite pagination in the HTTP request, still have a requested page to simplify code
4. set the total number of items
5. beeing able to easily tell the actual page to be displayed
    - this actual page will be called the current page and can be different from the requested page as the total number of items may have changed 
    (think about search criteria in the current request reducing this number)
6. a bean in the model which will be used by the template rendering framework of her choice to render any pagination related information
(except the data itself)
