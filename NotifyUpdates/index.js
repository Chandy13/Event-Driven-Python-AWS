'use strict';
var AWS = require("aws-sdk");
var sns = new AWS.SNS();

exports.handler = (event, context, callback) => {

    event.Records.forEach((record) => {
        console.log('Stream record: ', JSON.stringify(record, null, 2));

        if (record.eventName == 'INSERT') {
            var date = JSON.stringify(record.dynamodb.NewImage.Date.S);
            var cases = JSON.stringify(record.dynamodb.NewImage.Cases.N);
            var deaths = JSON.stringify(record.dynamodb.NewImage.Deaths.N);
            var recoveries = JSON.stringify(record.dynamodb.NewImage.Recoveries.N);
            var newcases = JSON.stringify(record.dynamodb.NewImage.New-Cases.N);
            var newdeaths = JSON.stringify(record.dynamodb.NewImage.New-Deaths.N);
            var newrecoveries = JSON.stringify(record.dynamodb.NewImage.New-Recoveries.N);
            var params = {
                Subject: 'Ontario Covid Data update',
                Message: `Successfully processed ${event.Records.length} records. On ${date}, there were ${newcases} cases, ${newdeaths} deaths, and ${newrecoveries} recoveries. In total there are ${cases} cases, ${deaths} deaths, and ${recoveries} recoveries`,
                TopicArn: 'arn:aws:sns:us-east-1:018943110893:NotifyMe'
            };
            sns.publish(params, function(err, data) {
                if (err) {
                    console.error("Unable to send message. Error JSON:", JSON.stringify(err, null, 2));
                } else {
                    console.log("Results from sending message: ", JSON.stringify(data, null, 2));
                }
            });
        }
    });
    callback(null, `Successfully processed ${event.Records.length} records.`);
};   