from hw_3.util import Writer

if __name__ == "__main__":
    writer = Writer()
    writer.write_results(level='ez')
    writer.write_results(level='medium')
    writer.write_hash_results()
