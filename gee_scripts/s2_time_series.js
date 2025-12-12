var roi = ee.Geometry.Polygon(
  [[[-1.382089, 7.391046],
    [-1.378977, 7.386684],
    [-1.374707, 7.389365],
    [-1.378999, 7.393429],
    [-1.382089, 7.391046]]],
  null, false
);

var addNDVI = function(img) {
  var ndvi = img.normalizedDifference(['B5', 'B4']).rename('NDVI');
  var EVI = img.expression('2.5 * ((B5 - B4) / (B5 + 6 * B4 - 7.5 * B2 + 1))', {
    'B5': img.select('B5'),
    'B4': img.select('B4'),
    'B2': img.select('B2')
  }).rename('EVI');
  return img.addBands(ndvi).addBands(EVI);
}
var s2 = ee.ImageCollection('COPERNICUS/S2_HARMONIZED').filterBounds(roi)
               .map(addNDVI);

var start_year = 2016;
var end_year = 2019;

var start_date = ee.Date.fromYMD(start_year, 1, 1);
var end_date = ee.Date.fromYMD(end_year + 1, 1, 1);

var years = ee.List.sequence(start_year, end_year);
var months = ee.List.sequence(1, 12);

var annual_ndvi = ee.ImageCollection.fromImages(
  years.map(function (year) {
    var annual = s2
                 .filter(ee.Filter.calendarRange(year, year, 'year'))
                 .median()
    return annual
           .set('year', year)
           .set('system:time_start', ee.Date.fromYMD(year, 1, 1));
}))

print(annual_ndvi);

var chart = ui.Chart.image.series({
  imageCollection:annual_ndvi.select(['NDVI', 'EVI']),
  region: roi,
  reducer: ee.Reducer.mean(),
  scale: 30,
  xProperty: 'system:time_start'}).setOptions({
    title: 'Annual Time-Series',
    vAxis: {title: 'value'},
    hAxis: {title: 'year'}
})

print(chart);

var monthly_ndvi = ee.ImageCollection.fromImages(
  years.map(function (y) {
    return months.map(function (m) {
      var w = s2.filter(ee.Filter.calendarRange(y, y, 'year'))
                      .filter(ee.Filter.calendarRange(m, m, 'month'))
                      .median();
      return w.set('year', y).set('month', m).set('system:time_start', ee.Date.fromYMD(y, m, 1));
    });
  }).flatten()
);

print(monthly_ndvi);

var chart = ui.Chart.image.series({
  imageCollection:monthly_ndvi.select(['NDVI']),
  region:roi,
  reducer:ee.Reducer.mean(),
  scale: 30,
  xProperty: 'system:time_start'}).setOptions({
    title: 'Monthly Time-Series',
    vAxis:{title:'value'},
    hAxis:{title:'month'},
})

print(chart);


