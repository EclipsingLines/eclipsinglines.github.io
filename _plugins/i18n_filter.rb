module Jekyll
  module I18nFilter
    def t(input)
      # Use the detected locale if available, otherwise fall back to the site's configured language
      lang = @context.registers[:page]['detected_locale'] || @context.registers[:site].config['detected_locale'] || @context.registers[:site].config['lang'] || 'en'
      
      # Load the translations for the detected locale
      translations = YAML.load_file("_data/translations/#{lang}.yml")
      
      # Return the translated text or the original text if no translation is found
      translations[input] || input
    end
  end
end

Liquid::Template.register_filter(Jekyll::I18nFilter)