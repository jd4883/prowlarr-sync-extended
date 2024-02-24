# Prowlarr Sync Extended

## Description
This is a small project written in python leveraging the various *arr API's in order to extend on the capabilities of prowlarr. As of this writing, there are two features I really wish prowlarr natively had that this will rectify. These are the following:

1. Configuring download clients and passing them across the various Apps. This is not super tedious but having parameters that are fed in and propagate to match is a nice perk.
2. Leveraging hidden settings in prowlarr, such as mapping a fixed download client to a given indexer and matching this in the other *arr apps.

The script is designed to be as light as possible on dependencies and to fit into a small docker container. Inputs will either be in the form of config files and/or envars. Secure handling of these is designed with kubernetes in mind but use the tool how it works best for you.

## Sample Configuration
```
```