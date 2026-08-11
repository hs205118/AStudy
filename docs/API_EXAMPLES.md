# API Examples

## 1. List modules

```bash
curl http://localhost:8000/api/v1/modules
```

## 2. Create run

```bash
curl -X POST http://localhost:8000/api/v1/runs -H 'Content-Type: application/json' -d '{"module_id":"storage-wizard","module_version":"1.0.0","parameters":{"product":"server-x"},"input_text":"Requires RAID 1 and 4 NVMe drives."}'
```

## 3. Extract IR

```bash
curl -X POST http://localhost:8000/api/v1/runs/$RUN_ID/execute
```

## 4. Edit IR

```bash
curl -X POST http://localhost:8000/api/v1/runs/$RUN_ID/ir/patch -H 'Content-Type: application/json' -d '{"patch":[{"op":"replace","path":"/entities/drive_count","value":8}],"comment":"Confirmed by engineer"}'
```

## 5. Generate and validate

```bash
curl -X POST http://localhost:8000/api/v1/runs/$RUN_ID/generate
```
