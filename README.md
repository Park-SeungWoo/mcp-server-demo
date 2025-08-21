## Main logics for framework-like server code
기구현 코드의 구조를 만든 메인 로직은 아래 파일들에 담겨있습니다.
- `core/bases/abstract_mcp_server.py`
- `core/bases/abstract_tool.py`
- `main.py`


## Run & Connect to the Servers

### Project Env Setting

`uv` 를 이용한 프로젝트 관리를 하고 있습니다.  
dependency 설치와 환경 세팅을 위해 아래 명령어를 실행합니다.

```shell
uv sync
```

### SSE Transport
SSE 서버는 아래 커맨드를 이용해 우선 서버를 실행 해야합니다.
```shell
uv run -s main.py -S DynamicToolManagementServer -T sse
```
이후 MCP client에서는 아래의 endpoint specifier로 해당 MCP 서버와 연결할 수 있습니다.

`http://localhost:8080/sse`

### STDIO Transport
STDIO 연결 방식을 선택할 경우 아래의 endpoint specifier를 MCP client에 등록해 연결할 수 있습니다.

`uv run --directory path/to/proj/root -s main.py -S FileServer`


## Command Line Options

| Option        | Alias | Description                    | Available value                                     | Default |
|---------------|-------|--------------------------------|-----------------------------------------------------|---------|
| `--list`      | `-L`  | Show available MCP Servers     | None                                                | None    |
| `--server`    | `-S`  | Select server to start         | Output of `-L` or [Here](#sample-servers-available) | None    |
| `--transport` | `-T`  | Select server transport option | `sse`, `stdio`                                      | `stdio` |


## Sample servers available

| Name                          | Path                  | Description                                                                                                                               |
|-------------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `SampleSSEServer`             | sample_sse/server.py  | Temporary server added while developing command-line transport option. Currently supports both SSE and STDIO transports for every server. |
| `FileServer`                  | file_server/server.py | Server to modify files on the host machine; primarily for testing STDIO transport.                                                        |
| `DBServer`                    | db_server/server.py   | Server connected to a PostgreSQL database with read-only tools.                                                                           |
| `DynamicToolManagementServer` | dynamic/server.py     | Server demonstrating dynamically changing tools.                                                                                          |

> [!IMPORTANT]
> DBServer requires starting a PostgreSQL container in advance using `docker-compose.db.yml`.  
> Simply, run `./start.sh` and `./stop.sh`


## Add New MCP Server

MCP Server는 각각 하나의 plugin으로 취급됩니다.  
모든 MCP Server는 특정 폴더 구조를 따라야 하며, 해당 구조만 포함된다면 어떠한 형태의 폴더, 파일의 추가도 허용됩니다.

### 1. 서버 폴더 구조

모든 서버는 `servers/` 내에서 별도의 폴더로 구분되는것이 권장되며, 다음 구조를 갖춰야 합니다.
```
servers/
├─ server_name/
│  ├─ prompts/
│  │  └─ init.py
│  ├─ resources/
│  │  └─ init.py
│  ├─ tools/
│  │  └─ init.py
│  └─ server.py
└─ file_server/
    └─ ...
```

> [!NOTE]  
> `prompts/` 와 `resources/` 는 현재 미구현 상태이며, 폴더 구조만 갖춰져 있습니다.  
> 필요할 경우 추후 구현할 예정입니다.

### 2. 서버 클래스 구현

- `server.py`에서 `core.bases.AbstractMcpServer`를 상속받아 서버 구현체 클래스를 작성합니다.  
- 클래스 이름은 서버 리스트와 서버 실행 시 **식별자**로 사용됩니다.  
- 필요한 경우 메서드를 재정의할 수 있으며, 단순히 클래스 선언만으로도 동작 가능합니다.

### 3. Tool 구현

- 모든 tool은 `core.bases.AbstractTool`을 상속받고 abstract method를 구현해야 합니다.

> [!NOTE]  
> 현재 prompt와 resource 인터페이스는 존재하지 않습니다.  
> `tools/` 폴더 내 모든 tool 클래스는 `tools/__init__.py`에서 import 되어야 합니다.

> [!IMPORTANT]  
> spec() 메서드를 재정의할 때 Tool 객체를 반환해야 하며, 이 과정에서 tool의 식별자로 이용되는 tool_name은 반드시 tool 클래스 이름의 **snake_case** 형태여야 합니다.  
> 따라서 클래스 이름은 tool 동작을 잘 설명하는 형태로 명명해야 합니다.

### 4. 패키지 구성

- `prompts/`, `resources/`, `tools/` 폴더는 반드시 패키지로 구성되어야 합니다.  
- 각 폴더의 `__init__.py`에서 모든 구현체를 import 해야 합니다.

### 5. 서버 등록

- 최종적으로 사용 가능한 서버는 `servers/__init__.py`에서 `./server_name/server.py`에 정의된 해당 서버 클래스를 import 해야 합니다.  
- `-L` 또는 `-S` 옵션으로 서버 정보를 확인할 때, 여기서만 정보를 가져오기 때문에 등록되지 않은 서버는 외부에 표시되지 않습니다.


## MCP Client
MCP 서버 연결 테스트는 postman을 이용해 수행할 수 있습니다.
