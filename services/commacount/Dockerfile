FROM golang:1.25-alpine AS build
WORKDIR /app
COPY . .
RUN go test ./... && CGO_ENABLED=0 go build -o /commacount .
FROM alpine:3.22
COPY --from=build /commacount /commacount
EXPOSE 8080
CMD ["/commacount"]
