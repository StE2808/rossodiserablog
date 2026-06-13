import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.toml' },
        miniflare: {
          d1Databases: { DB: 'test-db' },
          bindings: {
            TURNSTILE_SECRET: '1x0000000000000000000000000000000AA',
            ADMIN_TOKEN: 'testadmin',
            IP_SALT: 's',
          },
        },
      },
    },
  },
});
