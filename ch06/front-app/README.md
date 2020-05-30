# todo-app

Nuxt.js により構築されたアプリケーションです。

## Build Setup

``` bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

# API Endpointの設定

API Endpointは環境変数、またはnuxt.config.jsから指定します。

```
$ export API_ENDPOINT="https://xxxxxx.execute-api.<region>.amazonaws.com/v1/"
```

nuxt.config.jsから指定

```
  env: {
    apiEndPoint: process.env.API_ENDPOINT || "https://xxxxxx.execute-api.<region>.amazonaws.com/v1/"
  },
```
