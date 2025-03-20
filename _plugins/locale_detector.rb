module Jekyll
  class LocaleDetector < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      # Check for the lang query parameter in the URL
      require 'webrick'
      lang_param = WEBrick::HTTPUtils.parse_query(ENV['QUERY_STRING'])['lang']
      
      # If the lang parameter is present and valid, use it
      if lang_param && ['en', 'es'].include?(lang_param)
        preferred_lang = lang_param
      else
        # Otherwise, get the Accept-Language header from the environment
        accept_language = ENV['HTTP_ACCEPT_LANGUAGE'] || ''
        
        # Parse the Accept-Language header to get the preferred language
        # Format: language-tag;q=quality-value,language-tag;q=quality-value,...
        # Example: en-US,en;q=0.9,es;q=0.8
        languages = accept_language.split(',').map do |lang|
          lang_parts = lang.split(';q=')
          lang_tag = lang_parts[0].strip
          quality = lang_parts[1] ? lang_parts[1].to_f : 1.0
          [lang_tag, quality]
        end.sort_by { |_, quality| -quality }
        
        # Get the preferred language code (first two characters)
        preferred_lang = languages.first&.first&.split('-')&.first || site.config['lang'] || 'en'
      end
      
      # Check if the preferred language is supported
      supported_langs = Dir.glob("_data/translations/*.yml").map { |f| File.basename(f, '.yml') }
      
      # If the preferred language is not supported, fall back to the default language
      if !supported_langs.include?(preferred_lang)
        preferred_lang = site.config['lang'] || 'en'
      end
      
      # Set the detected locale in the site configuration
      site.config['detected_locale'] = preferred_lang
      
      # Make the detected locale available to all pages
      site.pages.each do |page|
        page.data['detected_locale'] = preferred_lang
      end
      
      # Make the detected locale available to all posts
      site.posts.docs.each do |post|
        post.data['detected_locale'] = preferred_lang
      end
      
      # Make the detected locale available to all collections
      site.collections.each do |_, collection|
        collection.docs.each do |doc|
          doc.data['detected_locale'] = preferred_lang
        end
      end
    end
  end
end