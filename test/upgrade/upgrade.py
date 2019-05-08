import os

def package_upgrade():
    package_yaml = "./manifests/devconsole/devconsole.package.yaml"
    fd = open(package_yaml)
    content = fd.readlines()
    fd.close()
    new_content = []
    for line in content:
        if line.strip().startswith("currentCSV"):
            new_line = line.split(".")[0:-1]
            new_line.append(str(int(line.split(".")[-1])+1))
            new_line =  ".".join(new_line)
            current_version = line.split(".",1)[-1][1:]
            new_version = new_line.split(".",1)[-1][1:]
            new_content.append(new_line)
        else:
            new_content.append(line)
    fd = open(package_yaml, "w")
    fd.write("".join(new_content))
    fd.write("\n")
    fd.close()
    return current_version.strip(), new_version.strip()

def csv_upgrade(current_version, new_version):
    current_csv = "./manifests/devconsole/" + current_version + "/devconsole-operator.v" + current_version + ".clusterserviceversion.yaml"
    new_csv = "./manifests/devconsole/" + new_version + "/devconsole-operator.v" + new_version + ".clusterserviceversion.yaml"
    os.mkdir("./manifests/devconsole/" + new_version)
    upgrade_yaml_block = open("./test/upgrade/upgrade_csv_block.yaml.txt").readlines()
    current_csv_content = open(current_csv).readlines()
    new_csv_content = []
    for line in current_csv_content:
        if line.strip() == "owned:":
            new_csv_content.append(line)
            new_csv_content.extend(upgrade_yaml_block)
            new_csv_content.extend("\n")
        else:
            new_csv_content.append(line)
    fd = open(new_csv, "w")
    fd.write("".join(new_csv_content))
    fd.write("\n")
    fd.close()



def upgrade():
    current_version, new_version = package_upgrade()
    csv_upgrade(current_version, new_version)

if __name__ == "__main__":
    upgrade()
