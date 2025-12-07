module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:import/recommended',
    'prettier',
  ],
  plugins: ['prettier', 'react'],
  rules: {
    'prettier/prettier': 'error',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  overrides: [
    // Define a custom override for MDX files
    {
      files: ['**/*.md', '**/*.mdx'],
      processor: '@docusaurus/eslint-plugin/markdown',
    },
    // Define a custom override for TypeScript files
    {
      files: ['**/*.{ts,tsx}'],
      parser: '@typescript-eslint/parser',
      extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:import/recommended',
        'prettier',
      ],
      plugins: [
        '@typescript-eslint',
      ],
      rules: {
        '@typescript-eslint/no-unused-vars': 'error',
        '@typescript-eslint/no-explicit-any': 'warn',
        '@typescript-eslint/explicit-function-return-type': 'off',
        '@typescript-eslint/no-use-before-define': 'off',
      },
    },
  ],
};