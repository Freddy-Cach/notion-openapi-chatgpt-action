# NotionGPT: Push and Pull Content from Your Notion Workspace with ChatGPT 🔥
Ever wished you could create Notion pages from ChatGPT? Have you wondered if there's an easy way your ChatGPT could be in sync with knowledge files in your Notion Workspace? 👀 Well, look no more! 

## Demo
https://github.com/user-attachments/assets/3713f886-cd77-49c5-b223-89a4942a4068

## Quickstart
### Setup for ChatGPT
1. Create a custom GPT and click ***Create new action***
2. Go to `https://notion-chatgpt.vercel.app` and click the copy button to get the `Import URL`.
3. Click "Authentication" and select `API-Key` using the `Bearer` authentication method
4. Head over to Notion Integrations and copy over your API-Key
5. Ensure this key has access to the workspace pages & databases you'd like to reference / update

## Raw Notion OpenAPI spec
Alternatively, you could copy this raw YAML (~300 lines)
```yaml
openapi: 3.1.0
info:
  title: Notion API
  description: API for interacting with Notion resources such as pages and databases.
  version: 1.0.0
servers:
- url: https://api.notion.com/v1
  description: Main API server
paths:
  /blocks/{block_id}:
    delete:
      responses: {}
      operationId: deleteBlock
    get:
      responses: {}
      operationId: retrieveBlock
    patch:
      responses: {}
      operationId: updateBlock
  /blocks/{block_id}/children:
    get:
      responses: {}
      operationId: retrieveBlockChildren
    patch:
      responses: {}
      operationId: appendBlockChildren
  /comments:
    get:
      responses: {}
      operationId: listComments
    post:
      responses: {}
      operationId: createComment
  /databases:
    post:
      responses: {}
      operationId: createDatabase
  /databases/{database_id}:
    get:
      responses: {}
      operationId: retrieveDatabase
    patch:
      responses: {}
      operationId: updateDatabase
  /databases/{database_id}/query:
    post:
      responses: {}
      operationId: queryDatabase
  /file_uploads:
    get:
      responses: {}
      operationId: listFileUploads
    post:
      responses: {}
      operationId: createFileUpload
  /file_uploads/{file_upload_id}:
    get:
      responses: {}
      operationId: retrieveFileUpload
  /file_uploads/{file_upload_id}/complete:
    post:
      responses: {}
      operationId: completeFileUpload
  /file_uploads/{file_upload_id}/send:
    post:
      responses: {}
      operationId: sendFileUpload
  /oauth/introspect:
    post:
      responses: {}
      operationId: introspectToken
  /oauth/revoke:
    post:
      responses: {}
      operationId: revokeToken
  /oauth/token:
    post:
      responses: {}
      operationId: createAccessToken
  /pages:
    post:
      responses: {}
      operationId: createPage
  /pages/{page_id}:
    get:
      responses: {}
      operationId: retrievePage
    patch:
      responses: {}
      operationId: updatePage
  /pages/{page_id}/properties/{property_id}:
    get:
      responses: {}
      operationId: retrievePagePropertyItem
  /search:
    post:
      responses: {}
      operationId: search
  /users:
    get:
      responses: {}
      operationId: listUsers
  /users/me:
    get:
      responses: {}
      operationId: retrieveBotUser
  /users/{user_id}:
    get:
      responses: {}
      operationId: retrieveUser
components:
  headers:
    NotionVersion:
      required: true
      schema:
        type: string
        default: '2022-06-28'
      description: Notion API version
  schemas:
    Page:
      type: object
      required:
      - object
      - id
      - properties
      properties:
        object:
          type: string
          enum:
          - page
        id:
          type: string
          format: uuid
        properties:
          type: object
          additionalProperties: true
    PageUpdate:
      type: object
      properties:
        properties:
          type: object
          additionalProperties: true
    PageCreate:
      type: object
      required:
      - parent
      - properties
      properties:
        parent:
          type: object
          required:
          - database_id
          properties:
            database_id:
              type: string
              format: uuid
        properties:
          type: object
          properties:
            title:
              type: array
              items:
                type: object
                properties:
                  text:
                    type: object
                    properties:
                      content:
                        type: string
          additionalProperties: true
        children:
          type: array
          items:
            type: object
            additionalProperties: true
        icon:
          type: object
          properties:
            emoji:
              type: string
        cover:
          type: object
          properties:
            external:
              type: object
              properties:
                url:
                  type: string
                  format: uri
    Database:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - database
        id:
          type: string
          format: uuid
        properties:
          type: object
          additionalProperties: true
    User:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - user
        id:
          type: string
          format: uuid
        name:
          type: string
        avatar_url:
          type: string
          format: uri
    BlockChildren:
      type: array
      items:
        $ref: '#/components/schemas/Block'
    Block:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - block
        id:
          type: string
          format: uuid
        type:
          type: string
        block_data:
          type: object
          additionalProperties: true
    Comment:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - comment
        id:
          type: string
          format: uuid
        parent:
          type: object
          additionalProperties: true
        content:
          type: string
    PagePropertyItem:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - property_item
        id:
          type: string
          format: uuid
        property_data:
          type: object
          additionalProperties: true
    DatabaseQuery:
      type: object
      properties:
        filter:
          type: object
          additionalProperties: true
        sorts:
          type: array
          items:
            type: object
            additionalProperties: true
    DatabaseRecord:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - database_record
        id:
          type: string
          format: uuid
        record_data:
          type: object
          additionalProperties: true
    SearchRequest:
      type: object
      properties:
        query:
          type: string
        sort:
          type: object
          additionalProperties: true
    SearchResponse:
      type: array
      items:
        $ref: '#/components/schemas/SearchResult'
    SearchResult:
      type: object
      required:
      - object
      - id
      properties:
        object:
          type: string
          enum:
          - search_result
        id:
          type: string
          format: uuid
        result_data:
          type: object
          additionalProperties: true
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
- BearerAuth: []
```
