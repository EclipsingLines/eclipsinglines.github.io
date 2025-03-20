module Jekyll
  module I18nFilter
    def t(input)
      lang = @context.registers[:site].config['lang']
      translations = YAML.load_file("_data/translations/#{lang}.yml")
      translations[input] || input
    end
  end
end

Liquid::Template.register_filter(Jekyll::I18nFilter)