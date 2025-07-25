from django.shortcuts import render
from django.core.serializers import serialize
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, response
from .serializers import *
from Coins_club_owner.models import *
from Coins_trader.models import *
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from datetime import datetime
from master.models import *
from User.models import *
from django.utils import timezone





class transfar1(APIView):
    sealizer_class = clubownerSerializer
    def post(self, request):
        serializer= self.sealizer_class(data=request.data)
        if serializer.is_valid():
            numcoin = serializer.validated_data.get('numcoin')
            owner_id = serializer.validated_data.get('Coins_Club_Owner_Id')
            print(f"Received owner_id: {owner_id}")  # Debugging
            try:
                club_owner = Coins_club_owner.objects.get(Name=owner_id)
                print(f"Found club_owner: {club_owner}")
                club_owner.coins += numcoin
                club_owner.save()
                transfer = Admin_to_Coins_club_owner.objects.create(Coins_Club_Owner_Id=club_owner, numcoin=numcoin,created_date=datetime.today())
                return Response({'total_coins': club_owner.coins,'message': 'Coins added successfully.'}, status=status.HTTP_201_CREATED)
            except Coins_club_owner.DoesNotExist:
                return Response({'error': 'Coins_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
            total_coins = club_owner.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid club_owner.'}, status=status.HTTP_400_BAD_REQUEST)


class CoinTransfer2(APIView):
    serializer_class = CointraderSerializer
    @method_decorator(authenticate_token) 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            trader_id = serializer.validated_data.get('to_trader')
            amount = serializer.validated_data.get('amount')
            try:
                owner = Coins_club_owner.objects.get(id=request.user.id)
                trader = Coins_trader.objects.get(Name=trader_id)
                owner_coins = owner.coins
                if owner_coins >= amount:
                    owner_coins -= amount
                    owner.coins = owner_coins
                    owner.save()
                    transfer = Coins_club_owner_to_Coins_trader.objects.create(from_owner=owner, to_trader=trader, amount=amount,created_date=datetime.today())
                    trader_coins = Coins_club_owner_to_Coins_trader.objects.filter(to_trader=trader).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if trader_coins is None:
                        trader_coins = 0
                    trader.coins = trader_coins
                    trader.save()
                    return Response({"total_coins": trader_coins, "message": "Coin transfer successful."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the owner account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_club_owner.DoesNotExist:
                return Response({'error': 'Coins_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            trader = Coins_trader.objects.get(uid=request.user.uid)
            total_coins = trader.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Coins_trader Token.'}, status=status.HTTP_400_BAD_REQUEST)




class CoinTransfer3(APIView):
    serializer_class = Jockey_club_ownerSerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():  
            jockey_owner_id = serializer.validated_data.get('to_Jockey_club_owner')
            amount = serializer.validated_data.get('amount')
            try:
                trader = Coins_trader.objects.get(id=request.user.id)
                jockey_owner = Jockey_club_owner.objects.get(Name=jockey_owner_id)
                trader_coins = trader.coins
                if trader_coins >= amount:
                    trader_coins -= amount
                    trader.coins = trader_coins
                    trader.save()
                    transfer = Coins_trader_to_Jockey_club_owner.objects.create(from_trader=trader, to_Jockey_club_owner=jockey_owner, amount=amount,created_date=datetime.today())
                    jockey_owner_coins = Coins_trader_to_Jockey_club_owner.objects.filter(to_Jockey_club_owner=jockey_owner).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if jockey_owner_coins is None:
                        jockey_owner_coins = 0
                    jockey_owner.coins = jockey_owner_coins
                    jockey_owner.save()
                    return Response({"total coins":jockey_owner_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the trader account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Jockey_club_owner.DoesNotExist:
                return Response({'error': 'Jockey_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            jokyclubowner = Jockey_club_owner.objects.get(uid=request.user.uid)
            total_coins = jokyclubowner.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Jockey_club_owner Token.'}, status=status.HTTP_400_BAD_REQUEST)

class CoinTransfer31(APIView):
    serializer_class = UserSerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('to_User')
            amount = serializer.validated_data.get('amount')
            try:
                trader = Coins_trader.objects.get(id=request.user.id)
                user = User.objects.get(Name=user_id)
                trader_coins = trader.coins
                if trader_coins >= amount:
                    trader_coins -= amount
                    trader.coins = trader_coins
                    trader.save()
                    transfer = Coins_trader_to_User.objects.create(from_trader=trader, to_User=user, amount=amount,created_date=datetime.today())
                    user_coins = Coins_trader_to_User.objects.filter(to_User=user).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if user_coins is None:
                        user_coins = 0
                    user.coins = user_coins
                    user.save()
                    return Response({"total coins":user_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the trader account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'user matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            wallet = User.objects.get(uid=request.user.uid)
            total_coins = wallet.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid User Token.'}, status=status.HTTP_400_BAD_REQUEST)

class CoinTransfer4(APIView):
    serializer_class = Audio_JockeySerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            audio_jockey_id = serializer.validated_data.get('to_Audio_Jockey')
            amount = serializer.validated_data.get('amount')
            try:
                audio_jockey = Audio_Jockey.objects.get(Name=audio_jockey_id)
                user = User.objects.get(id=request.user.id)
                user_coins = user.coins
                if user_coins >= amount:
                    user_coins -= amount
                    user.coins = user_coins
                    user.save()
                    transfer = User_to_Audio_Jockey.objects.create(from_User=user, to_Audio_Jockey=audio_jockey, amount=amount,created_date=datetime.today())
                    audio_jockey_coins = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audio_jockey).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if audio_jockey_coins is None:
                        audio_jockey_coins = 0
                    audio_jockey.coins = audio_jockey_coins
                    audio_jockey.save()
                    return Response({'total_coins': audio_jockey_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the Jockey_club_owner account.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Audio_Jockey.DoesNotExist:
                return Response({'error': 'Audio_Jockey matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            wallet = Audio_Jockey.objects.get(uid=request.user.uid)
            total_coins = wallet.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Audio_Jockey ID.'}, status=status.HTTP_400_BAD_REQUEST)
# transaction history


class clubownerpurchaseTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            Commn_user = Common.objects.get(uid=request.user.uid)
            club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
            followclaim = Follow_claim_coins.objects.filter(user=Commn_user)
            purchase = Purchase_history.objects.filter(user=Commn_user)
            daliylgin  = Coinsclubownerdaliylogin.objects.filter(user=club_owner)
            receivegift = GiftTransactionhistory.objects.filter(receiver=Commn_user)
            received_from_admin = Admin_to_Coins_club_owner.objects.filter(Coins_Club_Owner_Id=club_owner)
            all_transactions = list(received_from_admin) + list(receivegift) + list(followclaim) + list(purchase)  + list(daliylgin)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            Bonus_coins = 10 
            for transaction in all_transactions:
                if isinstance(transaction, Admin_to_Coins_club_owner):
                    transaction_type = "Received from Admin"
                    Coins_Club_Owner_Id = transaction.Coins_Club_Owner_Id.Name  
                    data = {
                        "transaction_type": transaction_type,
                        "Coins_Club_Owner_Id": Coins_Club_Owner_Id,
                        "amount": transaction.numcoin,
                        "created_date": transaction.created_date
                    }
                elif isinstance(transaction, Follow_claim_coins):
                    data = {
                    "transaction_type": "Received from_follow_10_user",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in receivegift: 
                        data = {
                            "transaction_type": f"Receive Gift as a {transaction.amount} coins! ",
                            "Received_from": transaction.sender.Name,
                            "created_date": transaction.created_date
                        }
                elif isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date
                        }
                elif isinstance(transaction, Coinsclubownerdaliylogin):
                    data = {
                    "transaction_type": "Received from_today_claim",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})
        

class clubownespendTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            Commn_user = Common.objects.get(uid=request.user.uid)
            club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
            send = Coins_club_owner_to_Coins_trader.objects.filter(from_owner=club_owner)
            sendgift = GiftTransactionhistory.objects.filter(sender=Commn_user)
            all_transactions = list(sendgift) + list(send)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Coins_club_owner_to_Coins_trader):
                    data = {
                        "transaction_type": "Paid to Cointrader",
                        "to_trader": transaction.to_trader.Name ,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in sendgift:
                        data = {
                            "transaction_type": f"Send Gift as a {transaction.amount} coins! ",
                            "send_to": transaction.receiver.Name,
                            "created_date": transaction.created_date
                            }
               
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})



class CointraderpurchaseTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:   
            trader = Coins_trader.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            followclaim = Follow_claim_coins.objects.filter(user=Commn_user)
            purchase = Purchase_history.objects.filter(user=Commn_user)
            daliylgin  = Coins_traderdaliylogin.objects.filter(user=trader)
            received = Coins_club_owner_to_Coins_trader.objects.filter(to_trader=trader)
            receivegift = GiftTransactionhistory.objects.filter(receiver=Commn_user)
            all_transactions = list(received) + list(purchase) + list(followclaim) + list(daliylgin) + list(receivegift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            Bonus_coins = 10
            for transaction in all_transactions:
                if isinstance(transaction, Follow_claim_coins):
                    data = {
                    "transaction_type": "Received from_follow_10_user",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }
                elif isinstance(transaction, Coins_traderdaliylogin):
                    data = {
                    "transaction_type": "Received from_today_claim",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, Coins_club_owner_to_Coins_trader):
                    from_owner = transaction.from_owner.Name
                    transaction_type = "Received from CoinClubowner"
                    data = {
                        "transaction_type": transaction_type,
                        "from_owner": from_owner,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in receivegift: 
                        data = {
                            "transaction_type": f"Receive Gift as a {transaction.amount} coins! ",
                            "Received_from": transaction.sender.Name,
                            "created_date": transaction.created_date
                        }
                elif isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date
                        }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})
        

class CointraderspendTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:   
            trader = Coins_trader.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            sendgift = GiftTransactionhistory.objects.filter(sender=Commn_user)
            sent_Jockey_club_owner = Coins_trader_to_Jockey_club_owner.objects.filter(from_trader=trader)
            sent_user = Coins_trader_to_User.objects.filter(from_trader=trader)
            all_transactions = list(sent_Jockey_club_owner) + list(sent_user) + list(sendgift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Coins_trader_to_Jockey_club_owner):  
                    data = {
                        "transaction_type": "Paid to Jockey_club_owner",
                        "to_Jockey_club_owner": transaction.to_Jockey_club_owner.Name  ,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }  
                       
                elif isinstance(transaction, Coins_trader_to_User): 
                    data = {
                        "transaction_type": "Paid to User",
                        "to_User": transaction.to_User.Name,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in sendgift:
                        data = {
                            "transaction_type": f"Send Gift as a {transaction.amount} coins! ",
                            "send_to": transaction.receiver.Name,
                            "created_date": transaction.created_date
                            }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})
        

class Jockey_club_ownerpurchaseTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            jockeyclubowner = Jockey_club_owner.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            followclaim = Follow_claim_coins.objects.filter(user=Commn_user)
            receivegift = GiftTransactionhistory.objects.filter(receiver=Commn_user)
            purchase = Purchase_history.objects.filter(user=Commn_user)
            daliylgin  = Jockeyclubownerlogin.objects.filter(user=jockeyclubowner)
            received = Coins_trader_to_Jockey_club_owner.objects.filter(to_Jockey_club_owner=jockeyclubowner)
            all_transactions = list(received) + list(purchase) + list(followclaim) + list(daliylgin) + list(receivegift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            Bonus_coins = 10
            for transaction in all_transactions:
                if isinstance(transaction, Coins_trader_to_Jockey_club_owner):
                    data = {
                        "transaction_type":"Received from Cointrader",
                        "from_trader": transaction.from_trader.Name,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }

                elif isinstance(transaction,  Follow_claim_coins):
                    data = {
                    "transaction_type": "Received from_follow_10_user",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, Jockeyclubownerlogin):
                    data = {
                    "transaction_type": "Received from_today_claim",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date
                        }
                    
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in receivegift: 
                        data = {
                            "transaction_type": f"Receive Gift as a {transaction.amount} coins! ",
                            "Received_from": transaction.sender.Name,
                            "created_date": transaction.created_date
                        }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})
        
        

#Audio_Jockey
class Audio_Jockey_and_Jockey_club_owner_spendTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try: 
            Commn_user = Common.objects.get(uid=request.user.uid)
            sendgift = GiftTransactionhistory.objects.filter(sender=Commn_user)
            all_transactions = list(sendgift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, GiftTransactionhistory):
                    if transaction in sendgift:
                        data = {
                            "transaction_type": f"Send Gift as a {transaction.amount} coins! ",
                            "send_to": transaction.receiver.Name,
                            "created_date": transaction.created_date
                            }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})
        

class Audio_JockeypurchaseTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try: 
            audiojockey = Audio_Jockey.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            followclaim = Follow_claim_coins.objects.filter(user=Commn_user)
            received = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audiojockey)
            roomcreate = room_create_claim_coins.objects.filter(user=audiojockey)
            receivegift = GiftTransactionhistory.objects.filter(receiver=Commn_user)
            purchase = Purchase_history.objects.filter(user=Commn_user)
            daliylgin  = Audiojockeyloigin.objects.filter(user=audiojockey)
            all_transactions = list(receivegift) + list(received) + list(purchase) + list(followclaim) + list(daliylgin) + list(roomcreate)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            Bonus_coins = 10
            for transaction in all_transactions:
                if isinstance(transaction, User_to_Audio_Jockey):     
                    data = {
                        "transaction_type": "Received from User",
                        "from_User": transaction.from_User.Name,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }

                elif isinstance(transaction,  Follow_claim_coins):   #Follow_claim_coins
                    data = {
                    "transaction_type":"Received from_follow_10_user",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, Audiojockeyloigin):
                    data = {
                    "transaction_type":"Received from_today_claim",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, room_create_claim_coins):
                    data = {
                    "transaction_type": "Received from_room_create",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date
                        }
                    
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in receivegift: 
                        data = {
                            "transaction_type": f"Receive Gift as a {transaction.amount} coins! ",
                            "Received_from": transaction.sender.Name,
                            "created_date": transaction.created_date
                        }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})




#USER_history        
class UserspendTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user = User.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            sendgift = GiftTransactionhistory.objects.filter(sender=Commn_user)
            sent = User_to_Audio_Jockey.objects.filter(from_User=user)
            all_transactions = list(sent) + list(sendgift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = [] 
            for transaction in all_transactions:
                if isinstance(transaction, User_to_Audio_Jockey):
                    data = {
                        "transaction_type": "Paid to Audio_Jockey",
                        "to_Audio_Jockey": transaction.to_Audio_Jockey.Name,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }

                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in sendgift:
                        data = {
                            "transaction_type": f"Send Gift as a {transaction.amount} coins! ",
                            "send_to": transaction.receiver.Name,
                            "created_date": transaction.created_date
                            }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})



class UserpurchaseTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user = User.objects.get(uid=request.user.uid)
            Commn_user = Common.objects.get(uid=request.user.uid)
            purchase = Purchase_history.objects.filter(user=Commn_user)
            receivegift = GiftTransactionhistory.objects.filter(receiver=Commn_user)
            follow_user_coins_received = Follow_claim_coins.objects.filter(user=Commn_user)
            room_join_received = room_join_claim_coins.objects.filter(user=user)
            received = Coins_trader_to_User.objects.filter(to_User=user)
            claim_coins_received = claim_coins.objects.filter(user=user)
            all_transactions = list(received) + list(follow_user_coins_received) + list(room_join_received) + list(claim_coins_received) + list(purchase)+ list(receivegift)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            Bonus_coins = 10 
            for transaction in all_transactions:
                if isinstance(transaction, Coins_trader_to_User):       
                    data = {
                        "transaction_type": "Received from Cointrader",
                        "from_trader": transaction.from_trader.Name,
                        "amount": transaction.amount,
                        "created_date": transaction.created_date
                    }
                elif isinstance(transaction, GiftTransactionhistory):
                    if transaction in receivegift: 
                        data = {
                            "transaction_type": f"Receive Gift as a {transaction.amount} coins! ",
                            "Received_from": transaction.sender.Name,
                            "created_date": transaction.created_date
                        }
                elif isinstance(transaction, Follow_claim_coins):
                    data = {
                    "transaction_type": "Received from_follow_10_user",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, room_join_claim_coins):
                    data = {
                    "transaction_type": "Received from_join_room",
                    "from_join_room": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }

                elif isinstance(transaction, claim_coins):
                    data = {
                    "transaction_type": "Received from_today_claim",
                    "today_claim": "Bonus coins",
                    "amount": Bonus_coins,  
                    "created_date": transaction.created_date
                    }
                elif isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date
                        }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
        except Exception as e:
            return Response({'error': f'{e}.'})


class AllUserpurchaseHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user = Common.objects.get(uid=request.user.uid)
            print(user.usertype)
            purchase = Purchase_history.objects.filter(user=user)
            all_transactions = list(purchase)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Purchase_history):
                    data = {
                        "transaction_type": "Received from_Recharge",
                        "today_claim": transaction.claim_coins, 
                        "created_date": transaction.created_date,
                        "User": serialize('json', [user])[58:65],
                        }
                else: 
                    continue
                transaction_data.append(data)
            if transaction_data:
                return Response({'message':transaction_data})
            else:
                return Response({"Transactions_History": 'No transactions available.'})
            
        except Exception as e:
            return Response({'error': f'{e}.'})

##############################################################################

class Top_fans_listing_globle_View(APIView):
    def get(self, request, id=None):
        try:
            audio_jockeys = Audio_Jockey.objects.all()
            total_coins_dict = {}
            for audio_jockey in audio_jockeys:
                received_transactions = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audio_jockey)
                sorted_transactions = received_transactions.order_by('-created_date')
                for transaction in sorted_transactions:
                    from_user_name = transaction.from_User.Name
                    coins = transaction.amount
                    if from_user_name in total_coins_dict:
                        total_coins_dict[from_user_name] += coins
                    else:
                        total_coins_dict[from_user_name] = coins

            vip_data = sorted(
                [{"from_User": user, "coins": total_coins} for user, total_coins in total_coins_dict.items()],
                key=lambda x: x["coins"],
                reverse=True
            )
            return Response({"top_list_user": vip_data})

        except User_to_Audio_Jockey.DoesNotExist:
            return Response({'error': 'No transactions received by any Audio_Jockey.'})

        except Exception as e:
            return Response({'error': str(e)})
        



class listofAudioJockey(APIView):
    def get(self, request):
        try:
            start_time_str = request.query_params.get('start_time')

            end_time_str = request.query_params.get('end_time')

            start_time = timezone.datetime.fromisoformat(start_time_str)

            end_time = timezone.datetime.fromisoformat(end_time_str)
            default_start_time = timezone.now() - timezone.timedelta(minutes=23)
            start_time = timezone.datetime.fromisoformat(start_time_str) if start_time_str else default_start_time

            end_time = timezone.datetime.fromisoformat(end_time_str) if end_time_str else timezone.now()

            audio_jockeys = Audio_Jockey.objects.all()

            for audio_jockey in audio_jockeys:
                total_coins = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audio_jockey,created_date__range=(start_time, end_time)).aggregate(total_coins=models.Sum('amount'))['total_coins'] or 0
                print("total_coins",total_coins)

                if total_coins is not None:
                    audio_jockey.coins = total_coins
                    

            audio_jockey_list = []

            for audio_jockey in audio_jockeys:
                jokey_data = {
                    "Audiojokey_id": audio_jockey.id,
                    "Audiojokey_Name": audio_jockey.Name,
                    "Audiojokey_Coin": audio_jockey.coins,
                }
                audio_jockey_list.append(jokey_data)

            sort_audio_jockeys = sorted(audio_jockey_list, key=lambda x: x['Audiojokey_Coin'], reverse=True)

            return Response({'Audio_jokey_list': sort_audio_jockeys})

        except Exception as e:
            return Response({'error': str(e)})





class TotalUserspendTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            Commn_user = Common.objects.get(uid=request.user.uid)
            sendgift = GiftTransactionhistory.objects.filter(sender=Commn_user)
            token=request.user
            total_spent_coins = 0
            username = ""
            usertype = ""
            profile_picture=""
            if isinstance(token , User):
                user = User.objects.get(uid=token.uid)
                username = user.Name
                usertype = user.usertype
                profile_picture = user.profile_picture
                sent = User_to_Audio_Jockey.objects.filter(from_User=user)
                all_transactions = list(sent) + list(sendgift)
                all_transactions.sort(key=lambda x: x.created_date, reverse=True)
                for transaction in all_transactions:
                    if isinstance(transaction, User_to_Audio_Jockey):
                        total_spent_coins += transaction.amount
                    elif isinstance(transaction, GiftTransactionhistory):
                        if transaction in sendgift:
                            total_spent_coins += transaction.amount
                    else: 
                        continue
            elif isinstance(token,Coins_trader):
                trader = Coins_trader.objects.get(uid=request.user.uid)
                username = trader.Name
                usertype = trader.usertype
                profile_picture = trader.profile_picture
                sent_Jockey_club_owner = Coins_trader_to_Jockey_club_owner.objects.filter(from_trader=trader)
                sent_user = Coins_trader_to_User.objects.filter(from_trader=trader)
                all_transactions = list(sent_Jockey_club_owner) + list(sent_user) + list(sendgift)
                all_transactions.sort(key=lambda x: x.created_date, reverse=True)
                for transaction in all_transactions:
                    if isinstance(transaction, Coins_trader_to_Jockey_club_owner):   
                        total_spent_coins += transaction.amount
                    elif isinstance(transaction, Coins_trader_to_User): 
                        total_spent_coins += transaction.amount
                    elif isinstance(transaction, GiftTransactionhistory):
                        if transaction in sendgift:
                            total_spent_coins += transaction.amount
                    else: 
                        continue
            elif isinstance(token, Audio_Jockey):
                AudioJockey = Audio_Jockey.objects.get(uid=request.user.uid)
                username = AudioJockey.Name
                usertype = AudioJockey.usertype
                profile_picture = AudioJockey.profile_picture
                all_transactions = list(sendgift)
                all_transactions.sort(key=lambda x: x.created_date, reverse=True)
                for transaction in all_transactions:
                    if isinstance(transaction, GiftTransactionhistory):
                        if transaction in sendgift:
                            total_spent_coins += transaction.amount
                    else: 
                        continue
            elif isinstance(token, Jockey_club_owner):
                Jockey = Jockey_club_owner.objects.get(uid=request.user.uid)
                username = Jockey.Name
                usertype = Jockey.usertype
                profile_picture = Jockey.profile_picture
                all_transactions = list(sendgift)
                all_transactions.sort(key=lambda x: x.created_date, reverse=True)
                for transaction in all_transactions:
                    if isinstance(transaction, GiftTransactionhistory):
                        if transaction in sendgift:
                            total_spent_coins += transaction.amount
                    else: 
                        continue
            elif isinstance(token,Coins_club_owner):
                club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
                username = club_owner.Name
                usertype = club_owner.usertype
                profile_picture = club_owner.profile_picture
                send = Coins_club_owner_to_Coins_trader.objects.filter(from_owner=club_owner)
                all_transactions = list(sendgift) + list(send)
                all_transactions.sort(key=lambda x: x.created_date, reverse=True)
                for transaction in all_transactions:
                    if isinstance(transaction, Coins_club_owner_to_Coins_trader):
                        total_spent_coins += transaction.amount
                    elif isinstance(transaction, GiftTransactionhistory):
                        if transaction in sendgift:
                            total_spent_coins += transaction.amount
                    else: 
                        continue
            vip_level = self.determine_vip_level(total_spent_coins,token)
            return Response({"username": username, "usertype": usertype,"profile_picture":profile_picture,"total_spend_coins":total_spent_coins,"vip_level": vip_level})
        except Exception as e:
            return Response({'error': f'{e}.'})
        
    def determine_vip_level(self, total_spent_coins,token):
        vip=10
        vip1=vip
        vip2=vip*2
        vip3=vip*3
        vip4=vip*4
        vip5=vip*5
        vip6=vip*6
        vip7=vip*7
        vip8=vip*8
        vip9=vip*9
        vip10=vip*10
        vip11=vip*11
        # vip6_frame="https://plus.unsplash.com/premium_photo-1663840297018-fe653527fc32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80"
        if total_spent_coins >= vip11:
                level = "vip11"
                self.determine_frame_vip_level(level,token)
                data={
                        "VIP_level": "VIP11", 
                        "Archive_level": "Congratulations! You have reached VIP level 11",
                        "message":"you succsefully Archive all vip_levels"
                        }
                return data
        elif total_spent_coins >= vip10:
                left=vip11-total_spent_coins
                level = "vip10"
                self.determine_frame_vip_level(level,token)
                next_level = f"You need {left} more coins to reach Next_VIP_level"
                data={
                        "VIP_level": "VIP10", 
                        "Archive_level": "Congratulations! You have reached VIP level 10",
                        "message":next_level
                        }
                return data
        elif total_spent_coins >= vip9:
            left=vip10-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_10"
            level = "vip9"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP9", 
                    "Archive_level": "Congratulations! You have reached VIP level 9",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip8:
            left=vip9-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_9"
            level = "vip8"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP8", 
                    "Archive_level": "Congratulations! You have reached VIP level 8",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip7:
            left=vip8-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_8"
            level = "vip7"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP7", 
                    "Archive_level": "Congratulations! You have reached VIP level 7",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip6:
            left=vip7-total_spent_coins
            level = "vip6"
            next_level = f"You need {left} more coins to reach VIP_level_7"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP6", 
                    "Archive_level": "Congratulations! You have reached VIP level 6",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip5:
            left=vip6-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_6"
            level = "vip5"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP5", 
                    "Archive_level": "Congratulations! You have reached VIP level 5",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip4:
            left=vip5-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_5"
            level = "vip4"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP4", 
                    "Archive_level": "Congratulations! You have reached VIP level 4",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip3:
            left=vip4-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_4"
            level = "vip3"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP3", 
                    "Archive_level": "Congratulations! You have reached VIP level 3",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip2:
            left=vip3-total_spent_coins
            next_level = f"You need {left} more coins to reach VIP_level_3"
            level = "vip2"
            self.determine_frame_vip_level(level,token)
            data={
                    "VIP_level": "VIP2", 
                    "Archive_level": "Congratulations! You have reached VIP level 2",
                    "message":next_level
                    }
            return data
        elif total_spent_coins >= vip1:
           left=vip2-total_spent_coins
           next_level = f"You need {left} more coins to reach VIP_level_2"
           level = "vip1"
           self.determine_frame_vip_level(level,token)
           data={
                    "VIP_level": "VIP1", 
                    "Archive_level": "Congratulations! You have reached VIP level 1", 
                    "message":next_level
                    }
           return data
        else:
            return "Regular"
        
    def determine_frame_vip_level(self,level,token):
        if level == "vip11":
            profile_frame = "vip11" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip10":
            profile_frame = "vip10" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip9":
            profile_frame = "vip9" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip8":
            profile_frame = "vip8" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip7":
            profile_frame = "vip7" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip6":
            profile_frame = "vip6" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip5":
            profile_frame = "vip5" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip4":
            profile_frame = "vip4" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip3":
            profile_frame = "vip3" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip2":
            profile_frame = "vip2" #self.vip6_frame
            self.frame_update(profile_frame,token)
        elif level == "vip1":
            profile_frame = "vip1" #self.vip6_frame
            self.frame_update(profile_frame,token)       
        
        
    def frame_update(self,profile_frame,token):
            user = Common.objects.get(uid=token.uid)
            user.profile_picture = profile_frame
            user.save()
            models=[User,Coins_club_owner,Coins_trader,Jockey_club_owner,Audio_Jockey]
            for model in models:
                if isinstance(token, model):
                    user = model.objects.get(uid=token.uid)
                    user.profile_picture = profile_frame
                    user.save()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gift
from .serializers import GiftSerializer

class GiftCreateAPIView(APIView):
    def post(self, request):
        serializer = GiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Gift
from .serializers import GiftSerializer

@api_view(['GET'])
def get_all_gifts(request):
    """
    Retrieve all gifts
    """
    try:
        gifts = Gift.objects.all()
        serializer = GiftSerializer(gifts, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Gifts retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)