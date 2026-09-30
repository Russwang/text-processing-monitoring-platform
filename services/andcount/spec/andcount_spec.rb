ENV['RACK_ENV'] = 'test'
require 'rack/test'
require_relative '../andcount'

RSpec.describe 'AndCount Service' do
  include Rack::Test::Methods

  def app
    Sinatra::Application
  end

  it 'returns correct count of "and"' do
    get '/', text: 'and and cloud and'
    expect(last_response).to be_ok
    response_body = JSON.parse(last_response.body)
    expect(response_body['answer']).to eq(3)
  end

  it 'returns 0 for no "and"' do
    get '/', text: 'hello world'
    expect(last_response).to be_ok
    response_body = JSON.parse(last_response.body)
    expect(response_body['answer']).to eq(0)
  end

  it 'is case insensitive' do
    get '/', text: 'AND And aNd'
    expect(last_response).to be_ok
    response_body = JSON.parse(last_response.body)
    expect(response_body['answer']).to eq(3)
  end

  it 'concatenated "and"' do
    get '/', text: 'andandand'
    expect(last_response).to be_ok
    response_body = JSON.parse(last_response.body)
    expect(response_body['answer']).to eq(0)
  end
end
