![メインブランチ CI](https://img.shields.io/badge/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%96%E3%83%A9%E3%83%B3%E3%83%81_CI-passing-brightgreen)
![CodeQL セキュリティ分析](https://img.shields.io/badge/CodeQL_%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E5%88%86%E6%9E%90-passing-brightgreen)
![OpenSSF Scorecard](https://img.shields.io/badge/openssf_scorecard-7.5-brightgreen)
![OpenSSF Best Practices](https://img.shields.io/badge/openssf_best_practices-silver-silver)
![ライセンス](https://img.shields.io/badge/%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9-MIT-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)

# Contoso OpenAI RAG エージェント

Azure OpenAI Service と検索拡張生成（RAG）を活用した、企業向けドキュメント Q&A インテリジェントチャットボットです。？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？

## アーキテクチャ

- **LangChain** - RAG パイプラインのオーケストレーション
- **FastAPI** - REST API エンドポイント
- **Azure OpenAI** (GPT-4) - 言語モデル
- **Azure Cognitive Search** - ベクターストア
- **Redis** - 会話メモリ

## クイックスタート

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API エンドポイント

- `POST /chat` - チャットボットにメッセージを送信
- `POST /upload` - RAG インデックス用のドキュメントをアップロード
- `GET /conversations/{id}` - 会話履歴を取得
- `DELETE /conversations/{id}` - 会話をクリア

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE)の下で公開されています。

## セキュリティ

脆弱性を発見された場合は、[セキュリティポリシー](SECURITY.md)をご確認ください。
