# Django - CRUD

> Django ORM을 활용하여 게시판 기능 구현하기

## 1. 환경설정

* 가상환경(venv)

  * python 3.7.4

* pip -`requirements.txt` 확인

  * 현재 패키지 리스트 작성

    ```bash
    $ pip freeze > requirements.txt
    ```

  * 만약, 다른 환경에서 동일하게 설치한다면

    ```bash
    $ pip install -r requirements.txt
    ```

* django app - `articles`(난 여기서 article이라 했어)

## 2. Model 설정

### 1. `Artile` 모델 정의

```python
# articles/models.py

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

* 클래스 정의할 때는 `models.Model`을 상속받아 만든다.

* 정의하는 변수는 실제 데이터베이스에서 각각의 필드(column)을 가지게 된다.

* 주요 필드

  * `CharField(max_length)`
    * 필수 인자로 `max_length`를 지정하여야 한다.
    * 일반적으로 데이터베이스에서 `VARCHAR` 로 지정된다.
    * `<input type="text">`
  * `TextField()`
    * 일반적으로 데이터베이스에서 `TEXT` 으로 지정된다.
    * `CharField` 보다 더 많은 글자를 저정할 때 사용된다.
    * `<textarea>`
  * `DateTimeField()`
    * 파이썬의 datetime 객체로 활용된다.
    * 옵션
      * `auto__now_add=True` : 생성시에 자동으로 저장(게시글 작성일)
      * `auto_now=True` : 변경시에 자동으로 저장(게시글 수정일)
  * `BooleanField()`, `FileField()`, `IntegerField()` 등 다양한 필드를 지정할 수 있다.

* `id` 값은 자동으로 `INTEGER` 타입으로 필드가 생성되고, 이는 `PK(Primary Key)` 이다.

* 모든 필드는 `NOT NULL` 조건이 선언되며, 해당 옵션을 수정하려면 아래와 같이 정의할 수 있다.

  ```python
  username = models.CharField(max_length=10, null=True)
  ```

### 2. 마이그레이션(migration) 파일 생성

> 마이그레이션(migration)은 모델에 정의한 내용(데이터베이스의 스키마)의 변경사항을 관리한다. 
>
> 따라서, 모델의 필드 수정 혹은 삭제 등의 변경될 때마다 마이그레이션 파일을 생성하고 이를 반영하는 형식으로 작업한다.

```bash
$ python manage.py makemigrations
Migrations for 'article':
  article\migrations\0001_initial.py
    - Create model Article
(venv)
# migrations 디렉토리 안에 0001_initial.py가 추가된다.
```

* 만약, 현재 데이터베이스에 반영되어 있는 마이그레이션을 확인하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py showmigrations
  article 
   [ ] 0001_initial # 반영되면 X 라고 표시된다.
  ```

### 3. DB 반영(migrate)

> 만들어진 마이그레이션 파일을 실제 데이터베이스에 반영한다.

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, article, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
```

* 만약 특정 app의 마이그레이션만 반영하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py migrate articles
  $ python manage.py migrate articles 0001
  ```

* 특정 마이그레이션 파일이 데이터베이스에 반영될 때 실행되는 쿼리문은 다음과 가이 확인할 수 있다.

  ```bash
  $ python manage.py sqlmigrate article 0001
  BEGIN;
  --
  -- Create model Article
  --
  CREATE TABLE "article_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(10) NOT NULL, "content" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
  COMMIT;
  ```

* 데이터베이스에 테이블을 만들 때, 기본적으로 `app이름_model이름` 으로 생성된다.

## 3. Django Query Methods

> Django ORM을 활용하게 되면, 파이썬 객체 조작으로 데이터베이스 조작이 가능한다.
>
> ORM(Obeject-Relational-Mapping)에서는 주로 활용되는 쿼리문들이 모두 method로 구성 되어있다.

```bash
$ python manage.py shell
$ python manage.py shell_plus
```

* `shell` 에서는 내가 활용한 모델 import 해야 한다.

  ```shell
  from article.models import Article
  ```

* `shell_plus` 는 `django_extensions` 를 설치 후 `INSTALLED_APPS`에 등록하고 활용해야 한다.

  ```bash
  $ pip install django-extensions
  ```

  ```python
  # crud/settings.py
  
  INSTALLD_APPS = [
      'django_extensions',
      ...
  ]
  ```

### 1. Create

```python
# 1. 인스턴스 생성 및 저장
article = Article()
article.title = "1번글"
article.content = '1번내용'
# article = Article(title='글', content='내용')
article.save()

# 2. create 메서드 활용
article = Article.objects.create(title='글', content='내용')
```

* 데이터베이스에 저장되면, `id` 값이 자동으로 부여된다. `.save()` 호출하기 전에는 `None` 이다.

### 2. Read

* 모든 데이터를 조회

  ```python
  Article.objects.all()
  ```

  * 리턴되는 값은 `QuerySet` 오브젝트
  * 각 게시글 인스턴스들을 원소로 가지고 있다.

* 특정(단일) 데이터 조회

  ```python
  Article.objects.get(pk=1)
  ```

  * 리턴되는 값은 `Article` 인스턴스
  * `.get()` 은 그 결과가 여러개 이거나 없는 경우 오류를 발생시킴
  * 따라서, 단일 데이터 조회시(primary key를 통해)에만 사용한다.

* 특정 데이터 조회

  ```python
  Article.objects.filter(title='제목1')
  Article.objects.filter(title__contains='제목') # 제목이 들어간 제목
  Article.objects.filter(title__startswith='제목') # 제목으로 시작하는 제목
  Article.objects.filter(title__enswith='제목') # 제목으로 끝나는 제목
  ```

  * 리턴되는 값은 `QuerySet` 오브젝트
  * `.filter()` 는 없는 경우/하나인 경우/여러개인 경우 모두 `QuerySet` 리턴

### 3. Update

```python
article = Article.objects.get(pk=1)
article.content = '내용 수정'
article.save()
```

* 수정은 특정 게시글을 데이터베이스에서 가져와서 인스턴스 자체를 수정한 후 `.save()` 호출.

### 4. Delete

```python
article = Article.objects.get(pk=1)
article.delete()
```

## 4. 기타

### 1. Limiting

```python
Article.objects.all()[0] # LIMIT 1 : 1개만
Article.objects.all()[2] # LIMIT 1 OFFSET 2
Article.objects.all()[:3]
```

### 2. Ordering

```python
Article.objects.order_by('-id') # id를 기준으로 내림차순 정렬
Article.objects.order_by('title') # title을 기준으로 오름차순 정렬
```





