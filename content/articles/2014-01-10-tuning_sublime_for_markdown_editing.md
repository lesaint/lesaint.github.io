Title: Tuning Sublime for markdown editing
Summary: Personnal notes for tuning Sublime Text 2
Tags: Sublime Text
category: articles

Here I keep a few notes on how to configure Sublime Text 2 to edit markdow editing.


# Markdown Editing in Sublime Text

- Excellent resource
  - [http://www.macstories.net/roundups/sublime-text-2-and-markdown-tips-tricks-and-links/](http://www.macstories.net/roundups/sublime-text-2-and-markdown-tips-tricks-and-links/)
- Install Sublime Text
  - see [Installing Sublime for my use]({filename}/articles/2014-01-08-installing_sublime_for_my_use.md)
- Extends Sublime for better editing experience (via Package Control)
  - Add package MarkdownEditing
    - installation
      + [http://ttscoff.github.com/MarkdownEditing/](http://ttscoff.github.com/MarkdownEditing/)
      + CTRL+SHIFT+P > Install Package
      + package name is "MarkdownEditing"
    - configuration
      + set "GitHub flavored Markdown" as default
        * open a Markdown file
        * select your flavor from the menu: View > Syntax > Open all with current extension as
      + overwrite few properties of MarkdownEditing to have black theme, not centered editing, no wrapping
        * open user preferences Preferences > Package Settings > MarkdownEditing > Markdown GFM Settings - User
        * change content with below

```json
        {
          "extensions":
          [
            "md",
            "mdown",
            "txt",
            "markdown"
          ],

          "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Dark.tmTheme",

          // Layout
          "draw_centered": false,
          "word_wrap": false,
          "wrap_width": 120
        }
```

  - Add Syntax highlighting sublime-markdown-extended (for reference, not used, MarkdownEditing is better)
    + [https://github.com/jonschlinkert/sublime-markdown-extended](https://github.com/jonschlinkert/sublime-markdown-extended)
    + CTRL+SHIFT+P > Install Package
    + package name is "Markdown Extended"
  - Add Color Theme Monokai Extended (not used for markdown, but good theme for other files)
    + [https://github.com/jonschlinkert/sublime-monokai-extended](https://github.com/jonschlinkert/sublime-monokai-extended)
    + CTRL+SHIFT+P > Install Package
    + package name is "Monokai Extended"
    + select as default color theme
      * Preferences > Color sheme > Monokai Extended > Monokai Extended
      * Bright sheme hurts my eyes


