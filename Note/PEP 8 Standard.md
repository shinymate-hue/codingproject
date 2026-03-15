파이썬의 공식 스타일 가이드인 **PEP 8**에서 요청하신 주요 항목들에 대한 핵심 요약과 예제입니다.

마크다운(Markdown) 표를 복사할 때 줄바꿈이나 공백이 깨지면 테이블이 제대로 렌더링되지 않을 수 있습니다.

특히 **`|` (수직 바)** 사이의 간격이나, 헤더 바로 밑의 **구분선(`| :--- |`)**이 정확하게 입력되어야 합니다. 복사해서 바로 사용하실 수 있도록 가장 표준적인 형태로 다시 작성해 드릴게요.

### 📋 PEP 8 가이드라인 요약 표

| 항목 | 핵심 규칙 요약 | 예제 코드 (Standard) |
| --- | --- | --- |
| **1. 들여쓰기** | 공백(Space) **4칸** 사용 (탭 금지) | `def func():` <br>

<br> `    print("4 spaces")` |
| **2. 공백** | 연산자 앞뒤 1칸, 괄호 안쪽은 금지 | `x = y + z` (O) <br>

<br> `x = (y+z)` (O) |
| **3. 빈 줄** | 최상위 간 **2줄**, 클래스 내 메서드 간 **1줄** | `class A:` <br>

<br> `    pass` <br>

<br> <br>

<br> `def B(): pass` |
| **4. 임포트** | 각 모듈은 별도의 줄에 작성 | `import os` <br>

<br> `import sys` |
| **5. 따옴표** | 한 종류를 선택해 일관되게 사용 | `s = 'Python'` <br>

<br> `s = "Python"` |
| **6. 네이밍** | 클래스는 `PascalCase`, 변수는 `snake_case` | `class MyClass:` <br>

<br> `user_id = 1` |
| **7. 함수명** | 소문자와 밑줄(`_`) 사용 | `def get_data():` <br>

<br> `    pass` |

---

### 💡 마크다운 표가 깨지는 이유와 해결 팁

만약 위 표를 복사해도 여전히 깨진다면 다음 두 가지를 확인해 보세요.

1. **앞뒤 빈 줄:** 표 위와 아래에 반드시 **한 줄 이상의 빈 줄**이 있어야 마크다운 엔진이 표로 인식합니다.
2. **구분선 누락:** `| :--- |` 로 시작하는 두 번째 줄(구분선)이 없으면 표가 만들어지지 않습니다.

이 표를 `.md` 파일에 붙여넣으실 때, 혹시 특정 에디터(VS Code, Obsidian 등)를 사용 중이신가요? 사용 환경을 알려주시면 그에 맞는 설정을 도와드릴 수 있습니다.

### 1. 들여쓰기 (Indentation)

* **원칙:** 공백(Space) **4칸**을 사용합니다. 탭(Tab)보다는 공백 사용을 권장하며, 두 방식을 섞어서 사용하면 안 됩니다.
* **예제:**
```python
# 올바름: 4칸 들여쓰기
def my_function():
    if True:
        print("Hello")

```

### 2. 공백 (Whitespace)

* **원칙:** 불필요한 공백은 피하되, 가독성을 위해 연산자 주변에 한 칸씩 사용합니다. 괄호 바로 안쪽에는 공백을 넣지 않습니다.
* **예제:**
```python
# 올바름
x = (y + z) * (a - b)

# 잘못됨
x = ( y + z ) * ( a-b ) 

```

### 3. 빈 줄 (Blank Lines)

* **원칙:** 최상위(Top-level) 함수와 클래스 정의 사이에는 **두 줄**을 띄웁니다. 클래스 내부의 메서드 사이에는 **한 줄**을 띄웁니다.
* **예제:**
```python
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass


def top_level_function():
    pass

```

### 4. 임포트 (Imports)

* **원칙:** 각 임포트는 별도의 줄에 작성하며, 파일의 맨 위(모듈 설명 및 docstring 다음)에 위치시킵니다.
* **예제:**
```python
# 올바름
import os
import sys
from subprocess import Popen, PIPE

```

### 5. 문자열 따옴표 (String Quotations)

* **원칙:** 작은따옴표(`'`)와 큰따옴표(`"`) 중 어느 것을 사용해도 무방하지만, 하나를 선택해 일관되게 사용합니다. 문자열 내에 따옴표가 포함된 경우, 백슬래시(`\`) 대신 다른 종류의 따옴표를 사용하여 가독성을 높입니다.
* **예제:**
```python
# 가독성 좋은 예
print("It's a beautiful day") 

```

### 6. 네이밍 컨벤션 (Naming Conventions)

* **클래스:** `CapWords` (PascalCase) 방식을 사용합니다.
* **변수:** `lower_case_with_underscores` (snake_case) 방식을 사용합니다.
* **상수:** `UPPER_CASE_WITH_UNDERSCORES` (대문자 스네이크 케이스)를 사용합니다.

### 7. 함수 이름 (Function Names)

* **원칙:** 변수와 마찬가지로 **소문자**로 작성하며, 가독성을 위해 필요한 경우 **밑줄(`_`)**로 단어를 구분합니다.
* **예제:**
```python
def calculate_total_price(amount, tax):
    return amount + tax

```
