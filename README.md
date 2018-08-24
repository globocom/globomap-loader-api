# GloboMap Loader API

Application responsible for reading connected applications events and apply them to the [Globo Map API](https://github.com/globocom/globomap-api).


## Starting Project:

` make dynamic_ports` <br>
` make containers_build ` (Build images.) <br>
` make containers_start ` (Up containers) <br>

## Running local with docker:

` make dynamic_ports` <br>
` make containers_build ` (When project not started yet.) <br>
` make containers_start ` (When project not started yet.) <br>

## Running Tests:

` make containers_build ` (When project not started yet.) <br>
` make containers_start ` (When project not started yet.) <br>
` make tests `

## Deploy in Tsuru:

### API

` make deploy_api project=<name of project> `<br>

## Environment variables configuration
All of the environment variables below must be set for the application to work properly.


### API
| Variable                           | Description                                                               | Example                                 |
|------------------------------------|---------------------------------------------------------------------------|-----------------------------------------|
| GLOBOMAP_RMQ_HOST                  | RabbitMQ host                                                             | rabbitmq.yourdomain.com                 |
| GLOBOMAP_RMQ_PORT                  | RabbitMQ port                                                             | 5672 (default)                          |
| GLOBOMAP_RMQ_USER                  | RabbitMQ user                                                             | user-name                               |
| GLOBOMAP_RMQ_PASSWORD              | RabbitMQ password                                                         | password                                |
| GLOBOMAP_RMQ_VIRTUAL_HOST          | RabbitMQ virtual host                                                     | /globomap                               |
| GLOBOMAP_RMQ_QUEUE_NAME            | RabbitMQ queue name                                                       | globomap-updates                        |
| GLOBOMAP_RMQ_EXCHANGE              | RabbitMQ updates exchange name                                            | globomap-updates-exchange               |
| GLOBOMAP_RMQ_ERROR_EXCHANGE        | RabbitMQ error exchange name                                              | globomap-errors-exchange                |
| GLOBOMAP_RMQ_BINDING_KEY           | RabbitMQ generic driver API binding key                                   | globomap.updates (default)              |
| DATABASE_POOL_SIZE                 | Relational database connection pool size                                  | 20 (default)                            |
| DATABASE_POOL_OVERFLOW             | Relational database connection pool overflow                              | 10 (default)                            |
| DATABASE_POOL_RECYCLE              | Number of seconds in which an idle connection is refreshed                | 120 (default)                           |
| SQLALCHEMY_DATABASE_URI            | The database URI that should be used for the connection                   | mysql://username:password@server/db     |
| VARIABLES of globomap-auth-manager | [globomap-auth-manager](https://github.com/globocom/globomap-auth-manager)| --                                      |

 ## Documentation
[API](https://github.com/globocom/globomap-core-loader/blob/master/doc/api.md)

## Licensing

GloboMap Core Loader is under [Apache 2 License](./LICENSE)
