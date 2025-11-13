# VLR API Project
Unofficial API for various data in VLR.gg
## API endpoints:
### Teams
#### **GET** `/team/compositions`
**Parameters:**

| Name        | Type     | Required | Default | Description                                                |
|-------------|----------|----------|---------|------------------------------------------------------------|
| `team_id`   | `string` | **Yes**  | —       | VLR ID of the team to fetch data for                       |
| `event_id`  | `string` | No       | `all`   | Fetch compositions for a specific event or all events      |
| `from_date` | `string` | No       | `None`  | Start date filter (`YYYY-MM-DD`)                           |
| `to_date`   | `string` | No       | `None`  | End date filter (`YYYY-MM-DD`)                             |

**Returns:**

Every team compositions played, and how many times, per map.


### Events
#### **GET** `/events`
**Parameters:**

| Name        | Type     | Required | Default | Permitted Values (if restricted)   | Description                                                |
|-------------|----------|----------|---------|------------------------------------|------------------------------------------------------------|
| `completed` | `bool` | No       | `true`  |                                    | Whether to fetch completed events (true), or upcoming events (false)|
| `page`  | `int` | No       | `1` |                                    | Page number for pagination      |
| `event_name_filter` | `string` | No       | `None`  |                                    | Filter events by name containing this string (case-insensitive)|
| `region`   | `string` | No       | `all`  |`all`, `americas`, `emea`, `pacific`, `china`|Region filter for events|
| `event_tier`   | `string` | No       | `all`  |`all`, `vct`, `vcl`, `tier3`, `gamechangers`, `collegiate`, `offseason`|Tier filter for events|

**Returns:**

One page of events and their details.
### Rankings
TBD

## Hosting an instance:
### Cloning the repository

1. **Clone the repository**

```bash
git clone https://github.com/jakubszmid1/vlrapi.git
cd vlrapi
```

### Running with docker:
#### 1. Build the Docker image

From the root of your project, run:

```bash
docker build -t vlrapi .
```

#### 2. Run the container and map port 8000
```bash
docker run -p 8000:8000 vlrapi
```
