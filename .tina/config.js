import { defineConfig } from "tinacms";

// Tina CMS Configuration
// Your hosting provider likely exposes this as an environment variable
const branch =
  process.env.GITHUB_BRANCH ||
  process.env.VERCEL_GIT_COMMIT_REF ||
  process.env.HEAD ||
  "main";

export default defineConfig({
  branch,

  // Get this from tina.io
  clientId: process.env.TINA_CLIENT_ID,
  // Get this from tina.io
  token: process.env.TINA_TOKEN,

  build: {
    outputFolder: "admin",
    publicFolder: "./",
  },
  media: {
    tina: {
      mediaRoot: "assets/images",
      publicFolder: "./",
    },
  },
  // See docs on content modeling for more info on how to setup new content models: https://tina.io/docs/schema/
  schema: {
    collections: [
      {
        name: "post",
        label: "Articoli",
        path: "_posts",
        format: "md",
        ui: {
          filename: {
            // Genera automaticamente il nome file con formato Jekyll: YYYY-MM-DD-titolo.md
            readonly: true,
            slugify: (values) => {
              const date = new Date(values?.date || new Date());
              const year = date.getFullYear();
              const month = String(date.getMonth() + 1).padStart(2, '0');
              const day = String(date.getDate()).padStart(2, '0');
              const slug = values?.title
                ?.toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/(^-|-$)/g, '') || 'nuovo-articolo';
              return `${year}-${month}-${day}-${slug}`;
            },
          },
        },
        fields: [
          {
            type: "string",
            name: "layout",
            label: "Layout",
            required: true,
            options: ["post"],
            ui: {
              component: "hidden",
            },
          },
          {
            type: "string",
            name: "title",
            label: "Titolo",
            isTitle: true,
            required: true,
          },
          {
            type: "datetime",
            name: "date",
            label: "Data Pubblicazione",
            required: true,
            ui: {
              dateFormat: "YYYY-MM-DD",
              timeFormat: "HH:mm:ss",
            },
          },
          {
            type: "string",
            name: "author",
            label: "Autore",
            required: true,
            options: ["lino-rialti", "ste2808"],
          },
          {
            type: "image",
            name: "image",
            label: "Immagine Copertina",
            description: "Immagine principale dell'articolo",
          },
          {
            type: "string",
            name: "tags",
            label: "Tag",
            list: true,
            description: "Aggiungi tag per categorizzare l'articolo",
          },
          {
            type: "string",
            name: "excerpt",
            label: "Sunto (50-300 caratteri)",
            description: "Breve descrizione per SEO e anteprima",
            ui: {
              component: "textarea",
            },
          },
          {
            type: "rich-text",
            name: "body",
            label: "Contenuto",
            isBody: true,
          },
        ],
      },
      {
        name: "author",
        label: "Autori",
        path: "_authors",
        format: "md",
        fields: [
          {
            type: "string",
            name: "layout",
            label: "Layout",
            required: true,
            options: ["author"],
            ui: {
              component: "hidden",
            },
          },
          {
            type: "string",
            name: "name",
            label: "Nome Completo",
            isTitle: true,
            required: true,
          },
          {
            type: "string",
            name: "bio",
            label: "Biografia",
            ui: {
              component: "textarea",
            },
          },
          {
            type: "string",
            name: "email",
            label: "Email",
          },
          {
            type: "image",
            name: "avatar",
            label: "Foto Profilo",
          },
          {
            type: "rich-text",
            name: "body",
            label: "Descrizione Estesa",
            isBody: true,
          },
        ],
      },
    ],
  },
});
