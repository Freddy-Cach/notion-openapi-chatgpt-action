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

## Creating a Database
When using `POST /databases` you must include a `properties` object. At least one property needs a `title` type. Here's a minimal example:

```json
{
  "parent": { "type": "page_id", "page_id": "YOUR_PAGE_ID" },
  "title": [{ "type": "text", "text": { "content": "Activity Logs" } }],
  "icon": { "type": "emoji", "emoji": "🪵" },
  "properties": {
    "Log": { "title": {} }
  }
}
```

Only basic property types (title, rich_text, number, select, multi_select, date,
people, files, checkbox, url, email, and phone_number) may be included at
creation time. More advanced types like `status`, `formula`, and `rollup` must be
added later using the update endpoint.

Add additional fields later with `PATCH /databases/{database_id}`:

```json
{
  "properties": {
    "Prompt": { "rich_text": {} },
    "Action": { "select": {} },
    "Timestamp": { "date": {} },
    "HTTP Status": { "number": {} }
  }
}
```

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
    get:
      responses: {}
    patch:
      responses: {}
  /blocks/{block_id}/children:
    get:
      responses: {}
    patch:
      responses: {}
  /comments:
    get:
      responses: {}
    post:
      responses: {}
  /databases:
    post:
      responses: {}
  /databases/{database_id}:
    get:
      responses: {}
    patch:
      responses: {}
  /databases/{database_id}/query:
    post:
      responses: {}
  /file_uploads:
    get:
      responses: {}
    post:
      responses: {}
  /file_uploads/{file_upload_id}:
    get:
      responses: {}
  /file_uploads/{file_upload_id}/complete:
    post:
      responses: {}
  /file_uploads/{file_upload_id}/send:
    post:
      responses: {}
  /oauth/introspect:
    post:
      responses: {}
  /oauth/revoke:
    post:
      responses: {}
  /oauth/token:
    post:
      responses: {}
  /pages:
    post:
      responses: {}
  /pages/{page_id}:
    get:
      responses: {}
    patch:
      responses: {}
  /pages/{page_id}/properties/{property_id}:
    get:
      responses: {}
  /search:
    post:
      responses: {}
  /users:
    get:
      responses: {}
  /users/me:
    get:
      responses: {}
  /users/{user_id}:
    get:
      responses: {}
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
          oneOf:
            - type: object
              required:
                - page_id
              properties:
                page_id:
                  type: string
                  format: uuid
            - type: object
              required:
                - database_id
              properties:
                database_id:
                  type: string
                  format: uuid
            - type: object
              required:
                - type
                - workspace
              properties:
                type:
                  type: string
                  enum:
                  - workspace
                workspace:
                  type: boolean
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
          oneOf:
            - type: object
              required:
                - type
                - emoji
              properties:
                type:
                  type: string
                  enum:
                  - emoji
                emoji:
                  type: string
            - type: object
              required:
                - type
                - external
              properties:
                type:
                  type: string
                  enum:
                  - external
                external:
                  type: object
                  properties:
                    url:
                      type: string
                      format: uri
        cover:
          oneOf:
            - type: object
              required:
                - type
                - external
              properties:
                type:
                  type: string
                  enum:
                  - external
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

## Troubleshooting validation errors
If you see a 400 `validation_error` complaining that `body.properties` should be an object or an `UnrecognizedKwargsError`, your JSON payload does not follow the creation schema. Ensure that:
- `parent` is present and correctly specifies the parent page ID.
- `title` is an array containing at least one `text` object.
- `properties` is a JSON object mapping property names to valid property definitions.
- Only creation-allowed property types are used; advanced types can be added later with `PATCH /databases/{id}`.
- The `Notion-Version` header is included.

Following these rules prevents those errors and allows the database to be created successfully.
