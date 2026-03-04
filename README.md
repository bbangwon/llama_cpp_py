Apple Silicon(MacBook Pro)에서 Metal 가속을 활성화하여 빌드하는 방법은 다음과 같습니다.

1. CMake 빌드 단계 (Metal 가속 포함)
   터미널에서 llama.cpp 폴더로 이동한 후 아래 명령어를 순서대로 입력하세요.

```Bash
# 1. 빌드 결과물을 담을 디렉토리 생성 및 이동
cmake -B build -DGGML_METAL=ON

# 2. 실제 컴파일 실행 (컴퓨터 성능에 따라 수 분 소요)
cmake --build build --config Release -j
```

- DGGML_METAL=ON: Apple Silicon의 GPU(Metal)를 사용하도록 설정하는 옵션입니다.
- j: 사용 가능한 CPU 코어를 모두 사용하여 빌드 속도를 높입니다.

2. 생성된 실행 파일 확인
   빌드가 완료되면 실행 파일들은 build/bin/ 폴더 안에 생성됩니다.

- CLI 도구: build/bin/llama-cli

- 서버 도구: build/bin/llama-server

잘 생성되었는지 확인하려면 다음 명령어를 입력해 보세요:

```Bash
ls -l build/bin/llama-cli
```

3. 모델 실행 방법 (예시)
   빌드된 파일을 사용하여 HyperCLOVA X 모델을 실행할 때는 경로를 build/bin/으로 지정해야 합니다.

```Bash
./build/bin/llama-cli -m [모델_파일_경로].gguf -p "반가워요, 자기소개 부탁해!" -n 128
```

4. 서버 실행 (예시)

```Bash
./build/bin/llama-server --model [모델_파일_경로].gguf --port 8080 -c 8192
```

- 서버 실행시 context size를 줄이면 메모리를 더 아낄수 있음
