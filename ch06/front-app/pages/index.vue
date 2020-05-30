<template>
  <v-row
    align="start"
    justify="center"
  >
    <v-col>
      <Column columnType="TODO" :taskList="toDoList"></Column>
    </v-col>
    <v-col>
      <Column columnType="INPROGRESS" :taskList="inProgressList"></Column>
    </v-col>
    <v-col>
      <Column columnType="DONE" :taskList="doneList"></Column>
    </v-col>
  </v-row>
</template>
<script>
  import { mapActions, mapGetters } from "vuex";
  import Column from '@/components/Column.vue'

  export default {
    components: {
      Column
    },
    computed: {
      ...mapGetters({
        toDoList: "tasks/toDoList",
        inProgressList: "tasks/inProgressList",
        doneList: "tasks/doneList",
      })
    },
    mounted: function() {
      this.fetchList();
    },
    methods: {
      ...mapActions({
        fetchList: "tasks/fetchList"
      })
    }
  }
</script>
