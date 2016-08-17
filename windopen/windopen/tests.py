from django.test import TestCase
from django.test import Client

class SteamViewTestCase(TestCase):
	def testSteam(self):
		resp = self.client.get('/windopen/steam/')
		self.assertEqual(resp.status_code, 200)

	def testSteamDiscountedGames(self):
		resp = self.client.get('/windopen/steamDiscountedGames/')
		self.assertEqual(resp.status_code, 200)

	def testSteamPlaytimeForever(self):
		resp = self.client.get('/windopen/steam/')
		for dict in resp.context:
			if 'playtime_forever' in dict:
				self.assertTrue('playtime_forever' in dict)

	def testSteamName(self):
		resp = self.client.get('/windopen/steam/')
		for dict in resp.context:
			if 'name' in dict:
				self.assertTrue('name' in dict)

	def testSteamImg(self):
		resp = self.client.get('/windopen/steam/')
		for dict in resp.context:
			if 'img_logo_url' in dict:
				self.assertTrue('img_logo_url' in dict)

	def testSteamAppID(self):
		resp = self.client.get('/windopen/steam/')
		for dict in resp.context:
			if 'appid' in dict:
				self.assertTrue('appid' in dict)

	def testSteamDiscountedGamesDiscount(self):
		resp = self.client.get('/windopen/steamDiscountedGames/')
		self.assertEqual(resp.context, None)


class windopenViewsTestCase(TestCase):
	def testIndex(self):
		resp = self.client.get('/windopen/api/')
		self.assertEqual(resp.status_code, 200)

	def testQuandlDowJones(self):
		resp = self.client.get('/windopen/quandlDowJones/')
		self.assertEqual(resp.status_code, 200)

	def testQuandlSnp500(self):
		resp = self.client.get('/windopen/quandlSnp500/')
		self.assertEqual(resp.status_code, 200)

	def testQuandlNasdaq(self):
		resp = self.client.get('/windopen/quandlNasdaq/')
		self.assertEqual(resp.status_code, 200)

	def testGithubUser(self):
		resp = self.client.get('/windopen/githubUser/')
		self.assertEqual(resp.status_code, 200)

	def testGithubTopRepositories(self):
		resp = self.client.get('/windopen/githubTopRepositories/')
		self.assertEqual(resp.status_code, 200)

	def testGithubResume(self):
		resp = self.client.get('/windopen/githubResume/')
		self.assertEqual(resp.status_code, 200)

	def testNytimespop(self):
		resp = self.client.get('/windopen/nytimespop/')
		self.assertEqual(resp.status_code, 200)

class YelpTestCase(TestCase):
	def testYelpPost(self):
		resp = self.client.post('/windopen/yelp/', {'location': 'yelp-san-francisco'})
		self.assertEqual(resp.status_code, 200)

	def testYelpContent(self):
		resp = self.client.post('/windopen/yelp/', {'location': 'yelp-san-francisco'})
		self.assertNotEqual(resp.content, '')

	def testYelpContentNotNone(self):
		resp = self.client.post('/windopen/yelp/', {'location': 'yelp-san-francisco'})
		self.assertIsNotNone(resp.content)

	def testGetYelpPage(self):
		resp = self.client.get('/windopen/yelp')
		self.assertEqual(resp.status_code, 301)

class ScraperTestCase(TestCase):
	def testScraperPage(self):
		resp = self.client.get('/windopen/steamDiscountedGames/')
		self.assertEqual(resp.status_code, 200)

	def testScraperContent(self):
		resp = self.client.get('/windopen/steamDiscountedGames/')
		self.assertNotEqual(resp.content, '')

class TwilioTestCase(TestCase):
	def testTwilio(self):
		resp = self.client.get('/windopen/twilio/')
		self.assertEqual(resp.status_code, 200)

	#def testMessage(self):
	#	resp = self.client.post('/windopen/twilio/', {'number': '+13473282978', 'message': 'hello world'})
	#	self.assertEqual(resp.status_code, 302)

class NewYorkTimesTestCase(TestCase):
	def testPopularArticles(self):
		resp = self.client.get('/windopen/nytimespop/')
		self.assertEqual(resp.status_code, 200)

	def testPopularArticlesContent(self):
		resp = self.client.get('/windopen/nytimespop/')
		self.assertNotEqual(resp.content, '')

	def testTopArticles(self):
		resp = self.client.get('/windopen/nytimestop/')
		self.assertEqual(resp.status_code, 200)

	def testTopArticlesContent(self):
		resp = self.client.get('/windopen/nytimestop/')
		self.assertNotEqual(resp.content, '')

	def testNewYorkTimesArticles(self):
		resp = self.client.get('/windopen/nytimesarticles/')
		self.assertEqual(resp.status_code, 200)

	def testNewYorkTimesArticlesContent(self):
		resp = self.client.get('/windopen/nytimesarticles/')
		self.assertNotEqual(resp.content, '')


