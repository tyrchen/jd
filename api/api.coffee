restify = require 'restify'
mongojs = require 'mongojs'
_ = require 'lodash'


db = mongojs 'directory'
employees = db.collection 'employees'
db_settings = db.collection 'settings'
items_per_page = 40

server = restify.createServer()

server.use restify.queryParser()
# server.use restify.jsonp()

server.get '/', (req, res, next) ->
	res.send
		status: 1

server.get '/employees.json', (req, res, next) ->
	employees.find().count (err, count) ->
		data = 
			total: count
			items: null

		if req.params.page
			data.page = parseInt req.params.page
		else
			data.page = 1

		options = {_id: 0, limit: items_per_page, skip: (data.page - 1) * items_per_page}

		employees.find {}, options, (err, docs) ->
			if docs
				data.items = docs
			res.send data 

server.get '/employees/:name', (req, res, next) ->
    uid = req.params.name.replace '.json', ''

    options = _id: 0
    employees.findOne {uid: uid}, options, (err, doc) ->
        res.send doc

server.get '/groups/:name', (req, res, next) ->
    uid = req.params.name.replace '.json', ''

    options = _id: 0
    data =
        total: 0
        members: null
    employees.findOne {uid: uid}, options, (err, doc) ->
        name = doc.preferred_name

        employees.find {manager: name}, options, (err, docs) ->
            if docs
                data.total = docs.length
                if req.params.uid
                    data.members = _.pluck docs, 'uid'
                else
                    data.members = docs
            res.send data

server.get '/search.json', (req, res, next) ->
    t = req.params.term.trim()
    if not t
        res.send []

    term = new RegExp t
    options = _id: 0
    query = "$or": [{uid: term}, {preferred_name: term}, {cube: term}, {extension: term}, {mobile: term}, {phone: term}]

    employees.find query, options, (err, docs) ->
        res.send docs

server.get '/snapshots.json', (req, res, next) ->
    # this API doesn't work till now
    db.getCollectionNames (err, names) ->
        data = _.map _.without(names, 'directory'), (item) -> item.replace('snapshot')

        res.send data

server.get '/gnats/monitored-group.json', (req, res, next) ->
    options = _id: 0

    db_settings.find {type: 'gnats-monitor-group'}, options, (err, docs) ->
        if docs.length == 1
            res.send docs[0].value
        else
            res.send []


server.listen 6080, ->
    console.log 'ready on %s', server.url