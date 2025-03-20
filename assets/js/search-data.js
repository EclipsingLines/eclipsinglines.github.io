// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-repositories",
          title: "repositories",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/repositories/";
          },
        },{id: "dropdown-news",
              title: "news",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/news/";
              },
            },{id: "dropdown-cv",
              title: "cv",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/cv/";
              },
            },{id: "post-godot-synth-release",
      
        title: "Godot Synth Release",
      
      description: "First public release of the Godot Synth Plugin",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/Synth-Release/";
        
      },
    },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-brand-new-website-sharing-my-code-for-games-tools-and-research",
          title: 'Brand new website, sharing my code for games, tools and research.',
          description: "",
          section: "News",},{id: "news-20240313-synth-release",
          title: '20240313 Synth Release',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/20240313-synth-release/";
            },},{id: "projects-project-faith",
          title: 'Project FAITH',
          description: "Faith is Active Inference for Thinking Humans",
          section: "Projects",handler: () => {
              window.location.href = "/projects/project_faith/";
            },},{id: "projects-godot-synth",
          title: 'Godot Synth',
          description: "Synthesizer plugin for godot, SFX and procedural music.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/project_synth/";
            },},{
        id: 'social-bluesky',
        title: 'Bluesky',
        section: 'Socials',
        handler: () => {
          window.open("https://bsky.app/profile/eclipsinglines.bsky.social", "_blank");
        },
      },{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%65%63%6C%69%70%73%69%6E%67%6C%69%6E%65%73.%63%6F%6E%74%61%63%74@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/EclipsingLines", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
