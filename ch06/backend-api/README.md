
# Backend API for TODO App

TODO Appで利用するAPIを構築します。  
CDK(python)を使用しています。


## 環境準備

AWS CDKのインストール

```
$ npm install -g aws-cdk
```

一度もAWS CDKを実行したことがない場合、Bootstrapが必要になります。

```
$ cdk bootstrap
```

Pipenvを利用していますので、pipenvをインストールしてください

```
$ pip install pipenv
```

依存関係のインストール

```
% pipenv install
```

## Lambda Packageの準備

Lambda functionは `api/lambda` ディレクトに配置しています。  
CDK内で `api/lambda` からパッケージを作成しますが、依存しているパッケージを事前に配置しておく必要があります。

```
$ cd api/lambda
$ pip install -r requirements.txt -t functions/vendor
```

## CDKの実行

```
$ cdk deploy
```
