require "rubygems"
require 'rake'
require 'yaml'
require 'time'

SOURCE = "."
CONFIG = {
  'version' => "0.3.0",
  'themes' => File.join(SOURCE, "_includes", "themes"),
  'layouts' => File.join(SOURCE, "_layouts"),
  'posts' => File.join(SOURCE, "_posts"),
  'drafts' => File.join(SOURCE, "_drafts"),
  'post_ext' => "md",
  'theme_package_version' => "0.1.0"
}

# Path configuration helper
module JB
  class Path
    SOURCE = "."
    Paths = {
      :layouts => "_layouts",
      :themes => "_includes/themes",
      :theme_assets => "assets/themes",
      :theme_packages => "_theme_packages",
      :posts => "_posts",
      :drafs => "_drafts"
    }

    def self.base
      SOURCE
    end

    # build a path relative to configured path settings.
    def self.build(path, opts = {})
      opts[:root] ||= SOURCE
      path = "#{opts[:root]}/#{Paths[path.to_sym]}/#{opts[:node]}".split("/")
      path.compact!
      File.__send__ :join, path
    end

  end #Path
end #JB

# Usage : rake draft title="A Title" [tags=[tag1, tag2]] [category="category"]
desc "Create a new draft in #{CONFIG['drafts']}"
task :draft do
  abort("rake aborted: '#{CONFIG['drafts']}' directory not found.") unless FileTest.directory?(CONFIG['drafts'])
  abort("rake aborted: missing title.") unless ENV["title"]
  title = ENV["title"] || "new-post"
  tags = ENV["tags"] || "[]"
  slug = title.downcase.strip.gsub(' ', '_').gsub(/[^\w-]/, '')
  filename = File.join(CONFIG['drafts'], "#{slug}.#{CONFIG['post_ext']}")
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end

  puts "creating a draft  #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts "tags:"
    post.puts " - "
    post.puts "categories:"
    post.puts " - articles"
    post.puts "image:"
    post.puts " feature: feature_image_green.png"
    post.puts "comments: false"
    post.puts "share: true"
    post.puts "---"
    # post.puts "{% include JB/setup %}"
  end
end # task draft

# Usage:
#   rake post title="A Title" [date="2012-02-09"] [tags=[tag1,tag2]] [category="category"]
#   rake post draft="some draft filename pattern"
desc "Begin a new post in #{CONFIG['posts']}"
task :post do
  abort("rake aborted: '#{CONFIG['posts']}' directory not found.") unless FileTest.directory?(CONFIG['posts'])

  if ENV['draft']
    postFromDraft(ENV['draft'])
  else
    newPost
  end
end # task :post


def postFromDraft(namePattern)
  puts "creation post from draft file with name pattern #{namePattern}"
  # 1/ look for file with the specified pattern in CONFIG['drafts'] directory
  # 2/ print for confirm
  # 3/ generate new name with date
  # 4/ copy to CONFIG['posts'] under new name
  # 5/ remove draft
end #postFromDraft

def newPost
  abort("rake aborted: missing title for new post") unless ENV["title"]
  title = ENV["title"]
  tags = ENV["tags"] || "[]"
  category = ENV["category"] || ""
  category = "\"#{category.gsub(/-/,' ')}\"" if !category.empty?
  slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  date = postDate
  filename = File.join(CONFIG['posts'], "#{date}-#{slug}.#{CONFIG['post_ext']}")
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end

  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts 'description: ""'
    post.puts "category: #{category}"
    post.puts "tags: #{tags}"
    post.puts "---"
    # post.puts "{% include JB/setup %}"
  end
end #newPost

# compute the date to add to the filename of a post for the current date
def postDate
  begin
    date = (ENV['date'] ? Time.parse(ENV['date']) : Time.now).strftime('%Y-%m-%d')
  rescue => e
    puts "Error - date format must be YYYY-MM-DD, please check you typed it correctly!"
    exit -1
  end
end #postDate

# Usage: rake page name="about.html"
# You can also specify a sub-directory path.
# If you don't specify a file extention we create an index.html at the path specified
desc "Create a new page."
task :page do
  name = ENV["name"] || "new-page.md"
  filename = File.join(SOURCE, "#{name}")
  filename = File.join(filename, "index.html") if File.extname(filename) == ""
  title = File.basename(filename, File.extname(filename)).gsub(/[\W\_]/, " ").gsub(/\b\w/){$&.upcase}
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end

  mkdir_p File.dirname(filename)
  puts "Creating new page: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: page"
    post.puts "title: \"#{title}\""
    post.puts 'description: ""'
    post.puts "---"
    post.puts "{% include JB/setup %}"
  end
end # task :page

desc "Launch preview environment"
task :preview do
  system "jekyll serve -w --draft"
end # task :preview

def ask(message, valid_options)
  if valid_options
    answer = get_stdin("#{message} #{valid_options.to_s.gsub(/"/, '').gsub(/, /,'/')} ") while !valid_options.include?(answer)
  else
    answer = get_stdin(message)
  end
  answer
end

def get_stdin(message)
  print message
  STDIN.gets.chomp
end

#Load custom rake scripts
Dir['_rake/*.rake'].each { |r| load r }
