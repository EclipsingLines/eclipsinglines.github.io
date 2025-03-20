module Jekyll
  class LocaleDetector < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      # Default to the site's configured language
      default_lang = site.config['lang'] || 'en'
      
      # Set the detected locale in the site configuration
      # This will be overridden by client-side JavaScript based on the cookie
      site.config['detected_locale'] = default_lang
      
      # Make the detected locale available to all pages
      site.pages.each do |page|
        page.data['detected_locale'] = default_lang
      end
      
      # Make the detected locale available to all posts
      site.posts.docs.each do |post|
        post.data['detected_locale'] = default_lang
      end
      
      # Make the detected locale available to all collections
      site.collections.each do |_, collection|
        collection.docs.each do |doc|
          doc.data['detected_locale'] = default_lang
        end
      end
      
      # Add the language-switcher.js script to the site's assets
      # This script will handle language switching on the client side
      site.static_files << Jekyll::StaticFile.new(
        site,
        site.source,
        'assets/js',
        'language-switcher.js'
      )
    end
  end
end