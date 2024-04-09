import yaml

from pathlib import Path

def get_files(directory, extension=".md"):
    files = list(Path(directory).rglob(f"*{extension}"))
    files = [f for f in files if '/.' not in str(f)]
    return files

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


class Note:
    def __init__(self, file_path):
        self.path = file_path
        self.yaml_text, self.document_body = Note._load_file(file_path)
        self.metadata = yaml.safe_load(self.yaml_text)

    def _load_file(file_path):
        with open(file_path, 'r') as f:
            yaml_data = ''
            in_yaml = False
            document_body = ''
            for line in f: 
                document_body += line
                if line == '---\n' and not in_yaml and yaml_data == '':
                    in_yaml = True
                    continue
                if line == '---\n' and in_yaml:
                    in_yaml = False
                    continue
                if in_yaml:
                    yaml_data += line + "\n"

            return yaml_data, document_body

    def save(self):
        document = "---\n" + yaml.dump(self.metadata, sort_keys=False, Dumper=IndentDumper) + "---\n"
        document += self.document_body.split('---\n')[-1]
        with open(self.path, "w") as f:
            f.write(document)
