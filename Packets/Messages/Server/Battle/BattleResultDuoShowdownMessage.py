from Utils.Writer import Writer
from Database.DatabaseManager import DataBase


class BattleResultDuoShowdownMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 23456
        self.player = player

    def encode(self):
        # Stuff
        brawler_trophies = self.player.brawlers_trophies[str(self.player.brawler_id)]
        brawler_trophies_for_rank = self.player.brawlers_trophies_in_rank[str(self.player.brawler_id)]
        if self.player.Brawler_starPower[str(self.player.brawler_id)] >= 1:
            brawler_level = self.player.Brawler_level[str(self.player.brawler_id)] + 2
        else:
            brawler_level = self.player.Brawler_level[str(self.player.brawler_id)] + 1
            
        # Rewards
        if self.player.tutorial <= 1:
            exp_reward = [0, 0, 0, 0, 0]
            token_list = [0, 0, 0, 0, 0]
            practice_exp_reward = [0, 0, 0, 0, 0]
            practice_token_list = [0, 0, 0, 0, 0]
            mvp_exp_reward = [0]
        else:
            exp_reward = [14, 8, 4, 2, 0]
            token_list = [32, 20, 8, 4, 0]
            practice_exp_reward = [7, 4, 2, 1, 0] 
            practice_token_list = [16, 10, 4, 2, 0] 
            mvp_exp_reward = [10]
            
        # Trophy Balance - ZMIENIONE WARTOŚCI DLA 2 MIEJSCA
        if 0 <= brawler_trophies <= 49:
            rank_1_val = 1250
            rank_2_val = 1000
            rank_3_val = 300
            rank_4_val = 0
            rank_5_val = 0
        else:
            if 50 <= brawler_trophies <= 499:
                rank_1_val = 1250
                rank_2_val = 1000
                rank_3_val = 4
                rank_4_val = 0
                rank_5_val = -1
            if 500 <= brawler_trophies <= 699:
                rank_1_val = 9
                rank_2_val = 500
                rank_3_val = 3
                rank_4_val = -1
                rank_5_val = -2
            if 700 <= brawler_trophies <= 899:
                rank_1_val = 9
                rank_2_val = 10
                rank_3_val = 2
                rank_4_val = 0
                rank_5_val = 0
            if 900 <= brawler_trophies <= 1000:
                rank_1_val = 9
                rank_2_val = -1000
                rank_3_val = 1
                rank_4_val = 0
                rank_5_val = 0
            if 1001 <= brawler_trophies <= 1099:
                rank_1_val = 5
                rank_2_val = 4
                rank_3_val = 0
                rank_4_val = 0
                rank_5_val = 0
            if 1100 <= brawler_trophies <= 1199:
                rank_1_val = 5
                rank_2_val = 4
                rank_3_val = 0
                rank_4_val = 0
                rank_5_val = 0
            if brawler_trophies >= 1200:
                rank_1_val = 4
                rank_2_val = 2
                rank_3_val = 0
                rank_4_val = 0
                rank_5_val = 0
                
        # Result Rewards 
        if self.player.result == 0:
            if self.player.battle_tokens <= 0 and self.player.collected_experience >= self.player.maximum_experience:
                result = self.player.result + 6
            elif self.player.battle_tokens <= 0:
                result = self.player.result + 4
            elif self.player.collected_experience >= self.player.maximum_experience:
                result = self.player.result + 2
            else:
                result = self.player.result
            gainedtrophies = 0
            if self.player.rank == 1:
                gainedtokens = practice_token_list[0]
                gainedexperience = practice_exp_reward[0]
                self.player.duo_wins += 1
                DataBase.replaceValue(self, 'duoWins', self.player.duo_wins)
            if self.player.rank == 2:
                gainedtokens = practice_token_list[1]
                gainedexperience = practice_exp_reward[1]
            if self.player.rank == 3:
                gainedtokens = practice_token_list[2]
                gainedexperience = practice_exp_reward[2]
            if self.player.rank == 4:
                gainedtokens = practice_token_list[3]
                gainedexperience = practice_exp_reward[3]
            if self.player.rank == 5:
                gainedtokens = practice_token_list[4]
                gainedexperience = practice_exp_reward[4]
        else:
            if self.player.rank in [1, 2]:
                if self.player.battle_tokens <= 0 and self.player.collected_experience >= self.player.maximum_experience:
                    result = self.player.result + 7
                elif self.player.battle_tokens <= 0:
                    result = self.player.result + 5
                elif self.player.collected_experience >= self.player.maximum_experience:
                    result = self.player.result + 3
                else:
                    result = self.player.result + 1
            else:
                if self.player.battle_tokens <= 0 and self.player.collected_experience >= self.player.maximum_experience:
                    result = self.player.result + 6
                elif self.player.battle_tokens <= 0:
                    result = self.player.result + 4
                elif self.player.collected_experience >= self.player.maximum_experience:
                    result = self.player.result + 2
                else:
                    result = self.player.result
            if self.player.rank == 1:
                gainedtokens = token_list[0]
                gainedexperience = exp_reward[0]
                gainedtrophies = rank_1_val
                self.player.duo_wins += 1
                DataBase.replaceValue(self, 'duoWins', self.player.duo_wins)
            if self.player.rank == 2:
                gainedtokens = token_list[1]
                gainedexperience = exp_reward[1]
                gainedtrophies = rank_2_val
            if self.player.rank == 3:
                gainedtokens = token_list[2]
                gainedexperience = exp_reward[2]
                gainedtrophies = rank_3_val
            if self.player.rank == 4:
                gainedtokens = token_list[3]
                gainedexperience = exp_reward[3]
                gainedtrophies = rank_4_val
            if self.player.rank == 5:
                gainedtokens = token_list[4]
                gainedexperience = exp_reward[4]
                gainedtrophies = rank_5_val
                
        if 0 <= result <= 15:
            starplayer = 1
        else:
            starplayer = 1
            
        # Star Player Info
        if starplayer == 5:
            starplayerexperience = mvp_exp_reward[0]
        else:
            starplayerexperience = 0
            
        # Results Balance
        if result in [0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27]:
            tokens = gainedtokens
        if result in [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31]:
            tokens = 0
        if result in [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29]:
            mvpexperience = starplayerexperience
            experience = gainedexperience
        if result in [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31]:
            mvpexperience = 0
            experience = 0
        if result in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]:
            startoken = 1
        if result in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
            startoken = 0
        if 0 <= result <= 31:
            trophies = gainedtrophies
            
        # DataBase Stuff             
        self.player.player_experience += experience + mvpexperience
        self.player.collected_experience += experience + mvpexperience
        if self.player.battle_tokens <= 0:
            token = 0
        if self.player.battle_tokens > tokens:
            token = tokens
        if tokens >= self.player.battle_tokens: 
            token = self.player.battle_tokens
        if self.player.tokenevent == 'true':
            tokenevent = token
        else:
            tokenevent = 0
        if self.player.tokensdoubler <= 0:
            doubledtokens = 0
        if self.player.tokensdoubler > token + tokenevent:
            doubledtokens = token + tokenevent
        if token + tokenevent >= self.player.tokensdoubler: 
            doubledtokens = self.player.tokensdoubler
        battle_tokens = self.player.battle_tokens - token
        remainingtokens = (self.player.tokensdoubler) - doubledtokens
        totaltokens = token + tokenevent + doubledtokens
        if self.player.coinevent == 'true':
            coinevent = totaltokens
        else:
            coinevent = 0
        new_gold = self.player.gold + coinevent
        new_trophies = self.player.trophies + trophies
        new_tokens = self.player.brawl_boxes + totaltokens
        new_startokens = self.player.big_boxes + startoken
        self.player.brawlers_trophies[str(self.player.brawler_id)] = brawler_trophies + trophies
        if self.player.brawlers_trophies_in_rank[str(self.player.brawler_id)] < self.player.brawlers_trophies[str(self.player.brawler_id)]:
            self.player.brawlers_trophies_in_rank[str(self.player.brawler_id)] = brawler_trophies + trophies
        if self.player.tutorial <= 1:
            pass
        else:
            DataBase.replaceValue(self, 'brawlersTrophies', self.player.brawlers_trophies)
            DataBase.replaceValue(self, 'brawlersTrophiesForRank', self.player.brawlers_trophies_in_rank)
            DataBase.replaceValue(self, 'trophies', new_trophies)
            DataBase.replaceValue(self, 'brawlBoxes', new_tokens)
            DataBase.replaceValue(self, 'bigBoxes', new_startokens)
            DataBase.replaceValue(self, 'availableTokens', battle_tokens)
            DataBase.replaceValue(self, 'tokensdoubler', remainingtokens)
            DataBase.replaceValue(self, 'playerExp', self.player.player_experience)
            DataBase.replaceValue(self, 'cappedExp', self.player.collected_experience)
            DataBase.replaceValue(self, 'gold', new_gold)
            DataBase.replaceValue(self, 'trp', self.player.trophiesanimation + gainedtrophies)
            
        self.writeVint(5) # Battle End Game Mode 
        self.writeVint(self.player.rank) # Result 
        self.writeVint(token) # Tokens Gained
        if self.player.result < 16:
            self.writeVint(0) # Trophies Result 
        if self.player.result >= 16:
            if gainedtrophies >= 0:
                self.writeVint(gainedtrophies) # Trophies Result
            if gainedtrophies < 0:
                self.writeVint(-65 - (gainedtrophies)) # Trophies Result
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(doubledtokens) # Doubled Tokens
        self.writeVint(tokenevent) # Double Token Event
        self.writeVint(remainingtokens) # Token Doubler Remaining
        self.writeVint(0) # Big Game/Robo Rumble Time
        self.writeVint(0) # Unknown (Championship Related)
        self.writeVint(0) # Championship Level Passed
        self.writeVint(0) # Challenge Reward Type (0 = Star Points, 1 = Star Tokens)
        self.writeVint(0) # Challenge Reward Ammount
        self.writeVint(0) # Championship Losses Left
        self.writeVint(0) # Championship Maximun Losses
        self.writeVint(coinevent) # Coin Shower Event
        self.writeVint(0) # Underdog Trophies
        if self.player.tutorial <= 1:
            self.writeVint(32) # Battle Result Type
        else:
            self.writeVint(result) # Battle Result Type
        self.writeVint(-64) # Championship Challenge Type
        self.writeVint(0) # Championship Cleared and Beta Quests
        
        # Players Array
        self.writeVint(self.player.players) # Battle End Screen Players
        self.writeVint(starplayer) # Team and Star Player Type
        self.writeScId(16, self.player.brawler_id) # Player Brawler
        self.writeScId(29, self.player.skin_id) # Player Skin
        self.writeVint(brawler_trophies) # Your Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        if self.player.tutorial <= 1:
            self.writeVint(brawler_level) # Your Brawler Power Level
        else:
            self.writeVint(10) # Your Brawler Power Level
        self.writeBoolean(True) # HighID and LowID Array
        self.writeInt(self.player.high_id) # HighID
        self.writeInt(self.player.low_id) # LowID
        self.writeString(self.player.name) # Your Name
        self.writeVint(self.player.player_experience) # Player Experience Level
        self.writeVint(28000000 + self.player.profile_icon) # Player Profile Icon
        self.writeVint(43000000 + self.player.name_color) # Player Name Color
            
        # Bots (1-9)
        for i in range(1, 10):
            bot_team = getattr(self.player, f'bot{i}_team')
            bot_id = getattr(self.player, f'bot{i}')
            bot_name = getattr(self.player, f'bot{i}_n')
            
            if bot_team == 0:
                self.writeVint(0)
            else:
                self.writeVint(2)
            self.writeScId(16, bot_id)
            self.writeVint(0)
            self.writeVint(0)
            self.writeVint(0)
            if self.player.tutorial <= 1:
                self.writeVint(1)
            else:
                self.writeVint(10)
            self.writeBoolean(False)
            self.writeString(bot_name)
            self.writeVint(0)
            self.writeVint(28000000)
            self.writeVint(43000000)
        
        # Experience Array
        self.writeVint(2)
        self.writeVint(0)
        self.writeVint(experience)
        self.writeVint(8)
        self.writeVint(mvpexperience)

        # Rank Up Bonus Array
        self.writeVint(0)

        # Trophies and Experience Bars Array
        self.writeVint(2)
        self.writeVint(1)
        self.writeVint(brawler_trophies)
        self.writeVint(brawler_trophies_for_rank)
        self.writeVint(5)
        self.writeVint(self.player.player_experience - experience - mvpexperience)
        self.writeVint(self.player.player_experience - experience - mvpexperience)
        
        self.writeScId(28, self.player.profile_icon)
        self.player.trophiesanimation = gainedtrophies
        if 16 <= result <= 23:
            self.writeBoolean(True)
        else:
            self.writeBoolean(False)
            
        if self.player.rank == 1:
            if self.player.tutorial <= 1:
                self.player.tutorial += 1
                DataBase.replaceValue(self, 'tutorial', self.player.tutorial)
                self.player.duo_wins -= 1
                DataBase.replaceValue(self, 'duoWins', self.player.duo_wins)