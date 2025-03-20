module Jekyll
  class LocaleContentLoader < Jekyll::Generator
    safe true
    priority :low  # Run after LocaleDetector

    def generate(site)
      # For each collection that might have translated content
      ['posts', 'news'].each do |collection_name|
        # Skip if the collection doesn't exist
        next unless site.collections.key?(collection_name)
        
        # Get the collection
        collection = site.collections[collection_name]
        
        # Get the original docs
        original_docs = collection.docs.dup
        
        # For each original doc
        original_docs.each do |doc|
          # Skip if the doc is already in Spanish
          next if doc.path.include?('/es/')
          
          # Construct the path to the Spanish version
          es_path = doc.path.sub("/_#{collection_name}/", "/_#{collection_name}/es/")
          
          # Skip if the Spanish version doesn't exist
          next unless File.exist?(es_path)
          
          # Read the Spanish version
          es_content = File.read(es_path)
          
          # Parse the front matter and content
          if es_content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)(.*)/m
            es_front_matter = YAML.safe_load($1)
            es_content = $4
          else
            es_front_matter = {}
          end
          
          # Create a new document with the Spanish content
          es_doc = Jekyll::Document.new(
            es_path,
            site: site,
            collection: collection
          )
          
          # Set the content and front matter
          es_doc.content = es_content
          es_doc.data.merge!(es_front_matter)
          
          # Set the URL to be the same as the original doc but with a language parameter
          es_doc.data['url'] = "#{doc.url}?lang=es"
          
          # Add the Spanish version to the collection (don't replace the original)
          collection.docs << es_doc
        end
      end
    end
  end
end