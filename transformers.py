from models import *




class BaseTransformer(object):
    def to_json(self,obj):
        pass
    def from_json(self,obj):
        pass

    def to_json_list(self,list):
        mylist = []
        for el in list:
            mylist.append(self.to_json(el))
        return mylist


class GuidelineFeedbackOverviewTransformer(BaseTransformer):
    def to_json(self,obj):
        if isinstance(obj,list):
            return self.to_json_list(obj);

        #resp = 100 * guideline.getNumberOfStoresWithResponses() / guideline.getConversations().size()
        convTrans = GuidelineConversationTransformer()
        return dict(guideline_id=obj.id,
            guideline_name=obj.name,
            guideline_due_date=obj.dueDate,
            response_rate=0,
            conversations=convTrans.to_json(obj.guidelineconversations))




class GuidelineConversationTransformer(BaseTransformer):
    def to_json(self,conv):
        if isinstance(conv,list):
            return self.to_json_list(conv)

        return dict(guideline_id=conv.guideline.id,
            store_id=conv.store_id,
            store_name=conv.store.name,
            store_address=conv.store.address,
            message_count=conv.messageCount,
            unread=conv.unread,
            update_date=conv.updateDate
        )

