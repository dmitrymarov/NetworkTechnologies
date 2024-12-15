# NetworkTechnologies
Структура проекта
mqtt-monitoring/
├── inv.yaml
├── deploy2.yml
├── roles/
│   ├── grafana/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   ├── grafana.ini.j2
│   │   │   ├── datasource.yml.j2
│   │   │   └── dashboard.yml
│   │   ├── files/
│   │   │   └── host.json
│   │   └── vars/
│   │		└── main.yml
│   ├── influxdb/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   └── tasks/
│   │       └── main.yml
│   ├── monitoring/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   ├── docker-compose.yml.j2
│   │   │   └── prometheus.yml.j2
│   │   └── files/
│   ├── mosquitto/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── templates/
│   │       └── mosquitto.conf.j2
│   └── telegraf/
│       ├── defaults/
│       │   └── main.yml
│       ├── tasks/
│       │   └── main.yml
│       └── templates/
│           └── telegraf.conf.j2

