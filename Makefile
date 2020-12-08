docker:
	docker build -t ytdl:latest .
	docker tag ytdl:latest localhost:5000/ytdl:latest
	docker push localhost:5000/ytdl:latest