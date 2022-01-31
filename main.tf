terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx_custom" {
  name = "nginx_custom"
  build {
    path = "${path.cwd}/nginx"
  }
}

resource "docker_image" "web" {
  name = "web"
  build {
    path = "${path.cwd}/web"
  }
}

resource "docker_image" "redis" {
  name = "redis:6.2.6-alpine"
}


resource "docker_container" "redis" {
  name = "service_redis"
  image = docker_image.redis.latest
  ports {
    internal = 6379
    external = 6379
  }
  networks_advanced {
    name = "docker_network"
    aliases = ["redis"]
  }
  ipc_mode = "shareable"

}

resource "docker_container" "web" {
  name = "service_web"
  image = docker_image.web.latest
  command = ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
  env = [
    "REF_JSON=dependencies/standard_payload.json",
    "TRANSFORMER_FILE=dependencies/data_transformer.pkl",
    "MODEL_FILE=dependencies/model.txt",
    "CACHE_TYPE=redis",
    "CACHE_REDIS_HOST=redis",
    "CACHE_REDIS_PORT=6379",
    "CACHE_REDIS_DB=0",
    "CACHE_REDIS_URL=redis://redis:6379/0",
    "CACHE_DEFAULT_TIMEOUT=500"
  ]
  networks_advanced {
    name = "docker_network"
    aliases = ["web"]
  }
  ipc_mode = "shareable"
}

resource "docker_container" "nginx_custom" {
  name = "service_nginx"
  image = docker_image.nginx_custom.latest
  ports {
    internal = 80
    external = 1337
  }
  networks_advanced {
    name = "docker_network"
    aliases = ["nginx"]
  }
  ipc_mode = "shareable"
}


resource "docker_network" "docker_network" {
  name = "docker_network"
}