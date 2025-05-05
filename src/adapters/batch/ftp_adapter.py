class FtpAdapter:
    def __init__(self, host, port, username, password, dispatcher):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dispatcher = dispatcher
        self.ftp = None

    def connect(self):
        import ftplib
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)

    def download_file(self, remote_file_path):
        local_file_path = f"/tmp/{remote_file_path.split('/')[-1]}"
        with open(local_file_path, 'wb') as local_file:
            self.ftp.retrbinary(f'RETR {remote_file_path}', local_file.write)
        return local_file_path

    def ingest(self, remote_file_path):
        self.connect()
        local_file_path = self.download_file(remote_file_path)
        self.dispatcher.route_data(local_file_path)
        self.ftp.quit()