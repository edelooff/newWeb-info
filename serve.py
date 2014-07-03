"""Starts a local development server for newWeb info."""

# Third-party modules
import uweb

# Application
import newweb_info


def main():
  app = newweb_info.main()
  app.serve()


if __name__ == '__main__':
  main()
