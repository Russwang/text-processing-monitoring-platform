require 'sinatra'
require 'sinatra/cross_origin'

configure do
  enable :cross_origin
end

before do
  response.headers['Access-Control-Allow-Origin'] = '*'
end

get '/' do
  text = params['text'] || ''
  and_count = text.scan(/\band\b/i).size
  content_type :json
  { answer: and_count }.to_json
end

options '/' do
  response.headers['Allow'] = 'GET,HEAD,POST,OPTIONS,PUT,DELETE'
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,POST,OPTIONS,PUT,DELETE'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Content-Length, X-Requested-With'
end
