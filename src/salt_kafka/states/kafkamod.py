__virtualname__ = "kafka"
__salt__ = {}
__opts__ = {}


def __virtual__():
    return True


def present(name, config=None):
    ret = {"name": name, "result": True, "comment": "", "changes": {}}

    if config is None:
        config = {}
    # The underlying Kafka client considers all config values as strings, so we
    # cast everything as string here to make things easier
    for key in config:
        config[key] = str(config[key])

    # Check if we need to create a new topic
    if name not in __salt__["kafka.list_topics"]():
        if __opts__["test"]:
            ret["comment"] = f"Topic {name} to be created"
            ret["result"] = None
            return ret
        elif __salt__["kafka.create_topic"](name, config=config):
            ret["changes"]["created"] = name
            ret["comment"] = f"Created topic {name}"
            return ret
        else:
            ret["comment"] = f"Topic {name} error"
            ret["result"] = False
            return ret

    # Check if we need to update the config
    existing_config = __salt__["kafka.describe_topic"](name)
    updated_config = {
        key: config[key] for key in config if config[key] != existing_config[key]
    }

    if updated_config:
        changed_config = __salt__["kafka.update_topic"](name, updated_config)
        for key in changed_config:
            ret["changes"][key] = (
                f"Changed {existing_config[key]} to {changed_config[key]}"
            )

    return ret


def absent(name):
    ret = {"name": name, "result": True, "comment": "", "changes": {}}
    topics = __salt__["kafka.list_topics"]()
    if name not in topics:
        ret["comment"] = f"Topic {name} is not present"
        return ret

    if __opts__["test"]:
        ret["comment"] = f"Topic {name} is set for removal"
        ret["result"] = None
    elif __salt__["kafka.delete_topic"](name):
        ret["changes"][name] = "Deleted"
        ret["comment"] = f"Removed topic {name}"
    else:
        ret["comment"] = f"Topic {name} error"
        ret["result"] = False
    return ret
