.. role:: shell(code)
   :language: shell

Описание
========

`Вступительное испытание`_ в `Школу бэкенд-разработки Яндекса`_ в 2022 году.

В проекте реализован бэкенд для веб-сервиса сравнения цен, аналогичный сервису
Яндекс Товары.

В сервисе реализованы следующие обработчики:

 **POST** /imports
Импортирует новые товары и/или категории.

 **DELETE** /delete/$id
Удаляет элемент по идентификатору.

 **GET** /nodes/$id
Получает информацию об элементе по идентификатору. При получении информации о категории также предоставляется информация о её дочерних элементах.

 **GET** /sales
Получение списка **товаров**, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от времени переданном в запросе.

Что внутри?
===========

Приложение упаковано в Docker-контейнер и разворачивается с помощью Ansible.

Внутри Docker-контейнера доступны две команды: :shell:`store-db` — утилита
для управления состоянием базы данных и :shell:`store-api` — утилита для
запуска REST API сервиса.

Как использовать?
=================
Как применить миграции:

.. code-block:: shell

    docker run -it \
        -e STORE_PG_URL=postgresql://user:hackme@localhost/store \
        dodir/backendschool2022 store-db upgrade head

Как запустить REST API сервис локально на порту 80:

.. code-block:: shell

    docker run -it -p 80:8081 \
        -e STORE_PG_URL=postgresql://user:hackme@localhost/store \
        dodir/backendschool2022

Опции для запуска можно указывать как аргументами командной строки, так и
переменными окружения с префиксом :shell:`STORE` (например: вместо аргумента
:shell:`--pg-url` можно воспользоваться :shell:`STORE_PG_URL`).

Как развернуть?
---------------
Чтобы развернуть и запустить сервис на серверах, добавьте список серверов в файл
deploy/hosts.ini (с установленной Ubuntu) и выполните команды:

.. code-block:: shell

    cd deploy
    ansible-playbook -i hosts.ini --user=root deploy.yml

Разработка
==========

Быстрые команды
---------------
* :shell:`make` Отобразить список доступных команд
* :shell:`make devenv` Создать и настроить виртуальное окружение для разработки
* :shell:`make postgres` Поднять Docker-контейнер с PostgreSQL
* :shell:`make lint` Проверить синтаксис и стиль кода с помощью `pylama`_
* :shell:`make clean` Удалить файлы, созданные модулем `distutils`_
* :shell:`make test` Запустить тесты
* :shell:`make sdist` Создать `source distribution`_
* :shell:`make docker` Собрать Docker-образ
* :shell:`make upload` Загрузить Docker-образ на hub.docker.com

.. _pylama: https://github.com/klen/pylama
.. _distutils: https://docs.python.org/3/library/distutils.html
.. _source distribution: https://packaging.python.org/glossary/

Как подготовить окружение для разработки?
-----------------------------------------
.. code-block:: shell

    make devenv
    make postgres
    source env/bin/activate
    store-db upgrade head
    store-api

После запуска команд приложение начнет слушать запросы на 0.0.0.0:8081.
Для отладки в PyCharm необходимо запустить :shell:`env/bin/store-api`.

Как запустить тесты локально?
-----------------------------
.. code-block:: shell

    make devenv
    make postgres
    source env/bin/activate
    pytest

Для отладки в PyCharm необходимо запустить :shell:`env/bin/pytest`.
