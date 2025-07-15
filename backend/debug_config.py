# debug_config.py
from dependency_injector import providers, containers

# Use the same absolute path you tried before
CONFIG_PATH = "/home/twardy/projects/Finance_calc/backend/config/config.yml"

class TempContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

if __name__ == "__main__":
    print(f"Attempting to load configuration from: {CONFIG_PATH}")
    container = TempContainer()
    try:
        container.config.from_yaml(CONFIG_PATH)
        print("\n✅ File loaded successfully!")
        print("Loaded configuration data:")
        print(container.config())

        print("\nValue of db.url:")
        print(container.config.db.url()) # Use () to get the value
    except Exception as e:
        print(f"\n❌ FAILED to load or parse the configuration file.")
        print(f"Error: {e}")