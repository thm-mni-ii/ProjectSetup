// eslint.config.js
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import globals from 'globals'
import vuePlugin from 'eslint-plugin-vue'
import tsPlugin from '@typescript-eslint/eslint-plugin'

import vueEslintParser from 'vue-eslint-parser'
import tsEslintParser from '@typescript-eslint/parser'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended
})

export default [
  ...compat.extends('eslint:recommended', 'plugin:vue/vue3-recommended', 'plugin:@typescript-eslint/recommended', 'prettier'),

  {
    ignores: ['node_modules/**', 'dist/**', '.git/**'],

    files: ['**/*.{js,jsx,cjs,mjs,ts,tsx,cts,mts,vue}'],

    languageOptions: {
      parser: vueEslintParser,

      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        parser: tsEslintParser,
        extraFileExtensions: ['.vue']
      },
      globals: {
        ...globals.browser,
        ...globals.node
      }
    },

    plugins: {
      vue: vuePlugin,
      '@typescript-eslint': tsPlugin
    },

    rules: {
      'vue/require-default-prop': 'off',
      'vue/no-mutating-props': 'warn'
    }
  }
]
