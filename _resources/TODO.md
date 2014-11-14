TODO javatronic.fr

# javatronic.fr

[X] tag page broken with redcarpet => liquid not understood ?
[X] fix author data and picture
[X] restore analytics (hardcoded in layout as before)
[X] add category article to existing posts => breaks links to pages => add link posts to provide forward
[X] add site logo
[X] formatted code not displayed with kramdown markdown processor (used redcarpet)
[X] change site title
[X] add link to Made Mistakes in footer (next to credit for theme)
[X] costumise copyright in footer
[X] add link to github and twitter in footer
[X] add link to tag page
[X] fix link convention to articles (must be same as before for google indexation)
[X] add feature image from all pages (until find a nice picture ?)
[X] enable comments on posts (via disqus)
[X] support for tag name with more than one word ? yes, use item list in front matter
[ ] find a way to add twitter link under my picture
[X] find a way to add summary to page
    - [ ] on top of the author, deployable layer?
    - [ ] control with a frontmatter variable
    - [-] enable extension of redcarpet to display TOC in articles 
    - [X] use kramdown
        - pour ajouter la toc dans un document
        
        ```
        * Table of Contents
        {:toc}
        ```

        - [X] modification css requise pour afficher plus d'un niveau car theme actuel ne supporte pas d'indentation
        - [X] modifier tous les blocs de code pour le support syntaxique

        ```
        # improved version, supports indented fenced blocks
        find . -name "*.md" -exec sed -i "s#^\(\s*\)\`\`\`\(\\w\+\)\$#\1\{\% highlight \2 \%\}#g" '{}' \;
        find . -name "*.md" -exec sed -i "s#^\(\s*\)\`\`\`\$#\1\{\% endhighlight \%\}#g" '{}' \;
        # http://stackoverflow.com/questions/9721253/sed-regex-substitute
        ```

        - [-] le code inline n'est plus rendu?
        - [X] autre différence de rendu?
[ ] re-enable paginator by adding the paginate option to config http://jekyllrb.com/docs/variables/#global-variables
[ ] page articles : add pagination (paginator does not seem to work anymore) ? display by month/year (see http://mmistakes.github.io/minimal-mistakes/posts/) ?
[X] modify RakeFile to include other Front-YAML properties (image feature, category articles)
[ ] modify RakeFile to create post from draft and automatically enable comment and put date in file name
[X] enable default extensions of redcarpet (http://stackoverflow.com/a/16126840)
[X] home : afficher 5 articles
[ ] home : afficher le excerpt et un lien lire la suite
[X] add link to home in navigation
[ ] add comment on source theme website about page tags broken with redcarpet
[ ] create a true DAMapping page, with posts from a category DAMapping + link to Github repo, online presentation, ...
[ ] leverage octopress because we now have a template of post (default value for feature image, comment, category)

# Annotation Processor articles

[X] vérifier le comportement si l'annotation Processor retourne la VERSION_7 et on compile pour JAVA_8
[ ] link to the JSR-269 as the reference of the Annotation Processing API
[ ] Talk about Annotation Processing instead of Annnotation Processor in text and titles (rename already published article)
[ ] Rename tag Annotation Processor to Annotation Processing
[ ] generated files are always overwritten when running an Annotation Processor (see javadoc of Filer)

# Tips

[ ] display Tips per Subject (Oracle, Sql, Cloud, ...) with abstract before the list of all Tips without abstract (see tags/index.md, not easy, dive into other properties offered by site object)
[X] split articles and tips in subdirectory inside `_post` directory

# minecraft

[X] replace "create new instance" by "create disk" and explain the disk will survive instances (because instances cost money)
[ ] find out how to use local world as server world
[ ] tune java
[ ] use whitelist.json to restrict connections
[ ] minecraft in Docker
    [ ] run as daemon
    [ ] world must be stored out of the Docker process
        - world directory be a symbolic link ?
        - can world directory configured to be somewhere else ?
[ ] install and use nc-minecraft (not exactly that name, check on work computer)
