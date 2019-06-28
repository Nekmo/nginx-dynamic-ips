
Docker-compose usage
====================

.. code-block::

  nginx-ips:
    build: https://github.com/Nekmo/nginx-dynamic-ips.git
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./data/nginx-ips/input:/input"
      - "/usr/bin/docker:/usr/bin/docker:ro"
    volumes_from:
      - "nginx"
    environment:
      OUTPUT_FILE: "/etc/nginx/allowed_ips.conf"
      LOOP_FOREVER: 10
      NGINX_CONTAINER: project_nginx_1
