**# CottagePilot 🏠

**A full-stack cottage management ecosystem integrating IoT monitoring, automated maintenance, and collaborative scheduling.**

CottagePilot was developed to solve a universal problem for shared property owners: the "nagging" friction of maintenance and the lack of transparency in property upkeep. This platform replaces subjective memory with objective data and automated workflows.



---

## 🚀 Overview

CottagePilot is a proactive property management tool that bridges the gap between physical property health and human coordination.

* **The Problem:** Maintenance tasks were often forgotten, responsibility was unclear, and environmental risks (like pipe bursts or mold) were only discovered after the damage was done.
* **The Solution:** A centralized hub where maintenance is triggered by real-time sensor data or pre-defined annual schedules, with an automated "enforcer" system to handle reminders.
* **The Goal:** A scalable SaaS product capable of handling multi-tenant cottage ownership.

---

## 🛠️ Tech

**##Tech Stach**
| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Vue.js 3, TypeScript, Tailwind CSS |
| **Backend** | Django, Django REST Framework (DRF), PostgreSQL |
| **IoT / Hardware** | ESP32 Microcontrollers, REST API (HTTP POST), C++/Arduino |
| **DevOps** | Docker, Docker Compose, Nginx |
| **SaaS Features** | Stripe Integration, Multi-tenant Authentication |

## Sensor Data Flow

The platform uses a robust, real-time data pipeline to ensure sensor readings are accurate, persistent, and instantly visible to users.

### Data Journey
1.  **Detection**: IoT sensors (e.g., ESP8266) read physical data (Temperature, Humidity).
2.  **Transmission**: Sensors publish encrypted JSON payloads to the **MQTT Broker** (Mosquitto).
3.  **Ingestion**: A Python **Bridge** service subscribes to MQTT and pushes raw data into a **Redis** queue.
4.  **Processing**: **Celery Workers** pick up batched data from Redis, validate it, provision new sensors (if needed), and bulk-save to **PostgreSQL**.
5.  **Real-Time Push**: Upon saving, a background task broadcasts the new data via **Django Channels** (WebSockets) to the specific cottage's group.
6.  **Visualization**: The Vue.js Frontend receives the WebSocket message and instantly updates the live line charts without a page reload.

### Architecture Diagram

```mermaid
graph LR
    S[Sensor Node] -->|MQTT| MB(MQTT Broker)
    MB -->|Sub| BR[Bridge Service]
    BR -->|Push| RQ[(Redis Queue)]
    RQ -->|Pull| CW[Celery Worker]
    CW -->|Bulk Save| DB[(PostgreSQL)]
    CW -.->|Broadcast| CL[Channel Layer]
    CL -->|WebSocket| FE[Frontend Vue.js]
    
    style S fill:#f9f,stroke:#333,stroke-width:2px
    style FE fill:#bbf,stroke:#333,stroke-width:2px
```


---

## ✨ Key Features

### 1. IoT Environmental Monitoring
The system integrates custom **ESP32 sensors** to monitor the property's vitals.
* **Real-time Telemetry:** Sensors report temperature and humidity every 5–15 minutes.
* **Automated Task Triggers:** If sensors detect threshold violations (e.g., freezing temperatures in winter), the backend automatically generates high-priority maintenance tasks.
* **Power Optimization:** Logic varies reporting frequency based on whether the unit is battery-powered or USB-C powered.

### 2. Automated Maintenance Logic
* **Objective Accountability:** Tasks are defined at the start of the season. If a task becomes overdue, the system sends automated email alerts to all owners. Removing the social awkwardness of one person having to "nag" others.
* **Priority Ranking:** Visual indicators for urgent vs. routine maintenance.

### 3. Collaborative Tools
* **Booking Calendar:** A conflict-free scheduling system for cottage visits.
* **The Leaderboard:** A social element featuring "biggest fish" tracking and shared grocery/repair notes to keep the family engaged.

### 4. SaaS Infrastructure
* **Multi-tenancy:** Architected to support multiple separate cottage groups.
* **Payment Gateway:** Integrated **Stripe** for handling subscription-based access.

---

## 📂 Project Structure

```text
COTTAGEPILOT_PUBLIC/
├── backend/                # Django REST Framework Root
│   ├── accounts/           # User authentication and profile management
│   ├── analytics/          # Data processing and usage insights
│   ├── calendarApp/        # Cottage visit scheduling logic
│   ├── cottageInstance/    # Multi-tenant property models
│   ├── notes/              # Shared notes and leaderboard system
│   ├── sensorhub/          # Django root folder
│   ├── sensors/            # Individual sensor configurations
│   ├── stripeApp/          # Subscription and payment integration
│   ├── tasks/              # Automated alerting, task scheduling and maintenance logic
│   ├── celery_app.py       # Asynchronous task queue configuration
│   ├── supervisord.conf    # Process control system configuration
│   └── manage.py           # Django CLI
├── esp_sensors/            # ESP32 firmware (C++ / Arduino / MicroPython)
├── frontend/               # Vue.js 3 + TypeScript source
│   ├── src/                # Component and view logic
│   ├── public/             # Static assets
│   ├── tailwind.config.js  # Styling configuration
│   ├── vite.config.ts      # Build tool configuration
│   └── package.json        # Frontend dependencies
├── nginx/                  # Web server and reverse proxy configuration
├── docker-compose.local.yml # Local orchestration configuration
└── README.md
**# CottagePilot 🏠

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tech Stack](https://img.shields.io/badge/stack-Vue3_Django_PostgreSQL-blue)
![IoT](https://img.shields.io/badge/IoT-ESP32_MQTT-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**A full-stack cottage management ecosystem integrating IoT monitoring, automated maintenance, and collaborative scheduling.**

CottagePilot was built to address the friction of shared property ownership: subjective maintenance "nagging", lack of transparency, and the risk of unnoticed environmental damage. By replacing memory with objective data and automated workflows, it transforms property upkeep into a managed, scalable process.

---

## 🚀 Overview

CottagePilot acts as the central nervous system for shared properties, bridging the gap between physical health and human coordination.

*   **The Problem:** Maintenance is often reactive. Pipes burst because heating fails unnoticed; tasks are forgotten; resentment builds over unequal workload distribution.
*   **The Solution:** A SaaS platform where real-time sensor data triggers automated maintenance tickets. "If temp < 5°C, create Urgent Task: 'Check Heating'."
*   **The Engineering Goal:** To build a robust, event-driven architecture capable of handling high-concurrency IoT ingestion while delivering millisecond-latency updates to the frontend.

---

## 🛠️ Tech Ecosystem

| Layer | Technologies | Role |
| :--- | :--- | :--- |
| **Frontend** | **Vue.js 3**, TypeScript, Tailwind CSS, Pinia | Reactive UI, state management, and real-time visualization. |
| **Backend** | **Django**, DRF, **Channels** (WebSockets) | REST API, Auth, and async event broadcasting. |
| **Data Layer** | **PostgreSQL**, **Redis** | Relational persistence and high-speed message buffering. |
| **IoT / Edge** | **ESP32** (C++/Arduino), **MQTT** | Telemetry capture and secure transmission. |
| **DevOps** | Docker, Nginx, Celery | Containerization, reverse proxying, and background worker orchestration. |

---

## 🏗️ System Architecture & Design Decisions

Designing for IoT requires handling asynchronous data flows that don't block the main application thread. Below is the event-driven pipeline implemented to ensure scalability.

### Architectural Decision Records (ADR)
*   **Decoupled Ingestion (MQTT + Bridge):** Instead of the Django app listening directly to sensors, an intermediate **MQTT Broker** and a lightweight **Python Bridge** buffer data into **Redis**. This prevents high-frequency sensor spikes from overwhelming the primary database.
*   **Hybrid Communication:** We use **REST** for standard CRUD (User management, Bookings) but **WebSockets (Django Channels)** for live sensor dashboards. This reduces server load by eliminating frontend polling.
*   **Asynchronous Persistence:** **Celery Workers** consume the Redis buffer in batches (`bulk_create`), optimizing database transactions.

### Data Flow Diagram

```mermaid
graph LR
    S[ESP32 Sensor] -->|JSON/MQTT| MB(Mosquitto Broker)
    MB -->|Sub| BR[Bridge Service]
    BR -->|LPUSH| RQ[(Redis Queue)]
    RQ -->|Pull Batch| CW[Celery Worker]
    CW -->|Bulk Insert| DB[(PostgreSQL)]
    CW -.->|Group Send| CL[Django Channels]
    CL -->|WebSocket| FE[Vue.js Frontend]
    
    style S fill:#f9f,stroke:#333,stroke-width:2px
    style FE fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 🧩 Key Engineering Challenges

### 1. Closing the Loop: Headless Sensor Provisioning
**Challenge:** How do you securely register a "headless" IoT device that has no UI/Keyboard?
**Solution:** Implemented a bi-directional provisioning flow.
1.  Unregistered sensors publish to `sensors/data` with a default code.
2.  The backend detects the new ID, generates a cryptographically secure `code`, and creates a pending record.
3.  The backend publishes the new code back to `sensors/provision/{sensor_id}` via MQTT.
4.  The sensor listens for this specific topic, writes the code to EEPROM, and uses it for all future authenticated transmissions.

### 2. Bridging Async Workers with Real-Time Sockets
**Challenge:** `Celery` workers (running in a separate process) save data to the DB, but the `WebSocket Consumer` (Daphne) needs to know about it instantly to update the UI.
**Solution:** Leveraged the `channel_layer` (Redis-backed) within the Celery task. Immediately after a DB commit, the worker broadcasts a standardized JSON payload to the specific `sensors_group_{cottage_id}`, enabling a seamless "Database -> UI" sync without HTTP overhead.

### 3. Multi-Tenant Data Isolation
**Challenge:** Ensuring Sensor A's data is only visible to Cottage B's owners.
**Solution:** Implemented strict Group-Based Access Control (GBAC). WebSocket connections are authenticated via Token and assigned to specific Channel Groups based on the user's `CottageInstance` association. Data is routed strictly to these groups, preventing cross-tenant data leakage.

---

## ✨ Key Features

### 1. IoT Environmental Monitoring
*   **Real-time Telemetry:** Live charts for Temperature, Humidity, and Pressure.
*   **Automated Triggers:** "Smart Tasks" are generated automatically when environmental thresholds are breached.

### 2. Automated Maintenance Logic
*   **Objective Accountability:** Usage-based or time-based maintenance schedules.
*   **Escalation:** System auto-emails owners when high-priority tasks are overdue.

### 3. Collaborative Tools
*   **Conflict-Free Booking:** Visual calendar for managing shared custody.
*   **Notes:** Track contributions, missing tools and note-taking.

---

## 📂 Project Structure

```text
COTTAGEPILOT_ROOT/
├── backend/                # Django REST Framework Monorepo
│   ├── sensorhub/          # Project settings & routing
│   ├── sensors/            # Sensor logic & WebSocket consumers
│   ├── tasks/              # Celery tasks & Automation rules
│   ├── mqtt_to_redis.py    # Ingestion Bridge Service
│   └── ...
├── esp_sensors/            # Embedded C++ Firmware
├── frontend/               # Vue.js 3 SPA
│   ├── src/stores/         # Pinia Stores (State)
│   ├── src/views/          # Views (Dashboard, Analytics)
│   └── ...
├── nginx/                  # Production Reverse Proxy
└── docker-compose.yml      # Container Orchestration
```

---

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Node.js 18+ (for local frontend dev)

### Quick Launch (Docker)
1.  **Clone & Configure:**
    ```bash
    git clone https://github.com/sonofpeter-git/CottagePilot.git
    cp backend/.local.env.example backend/.local.env
    ```
2.  **Ignition:**
    ```bash
    docker compose -f docker-compose.local.yml up --build
    ```
3.  **Access:**
    *   Frontend: `http://localhost:8080`
    *   API / Admin: `http://localhost:8000`

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.
