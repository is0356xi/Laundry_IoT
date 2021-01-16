<template>
  <div>
    <v-row>
      <table cellspacing="4">
        <thead></thead>
        <tbody>
          <tr>
            <td v-for="data in limitCount" :key="data.hour">
              <v-card max-width="250">
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title class="title">
                      {{ data.hour }}:00
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>

                <v-card-text>
                  <v-row align="center">
                    <v-col
                      class="subtitle-1"
                      cols="4"
                    >
                      23&deg;C
                    </v-col>
                    <v-col cols="4">
                      <img :src="'/static/img/laundry/0'+ data.laundry_index + '.png'"
                        width="70"
                      />
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-list-item two-line>
                  <div>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon small>mdi-send</v-icon>
                        <v-list-item-subtitle class="pl-2">{{ data.windSpeed }} m/s</v-list-item-subtitle>
                      </v-list-item-icon>
                    </v-list-item>

                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon small>mdi-cloud-download</v-icon>
                        <v-list-item-subtitle class="pl-2">{{ data.rainfall }} mm/h</v-list-item-subtitle>
                      </v-list-item-icon>
                    </v-list-item>
                  </div>
                  <div>
                    <v-list-item>
                      <figure>
                        <img
                          :src="'/static/img/weatherIcon/' + data.weather + '.png'"
                          width="60"
                        />
                        <figcaption>{{ data.weather }}</figcaption>
                      </figure>
                    </v-list-item>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
              </v-card>
            </td>
          </tr>
        </tbody>
      </table>
    </v-row>
  </div>
</template>

<script>
const axios = require('axios').create()
export default {
  name: 'weather',
  data () {
    return {
      tableData: []
    }
  },
  mounted () {
    this.getWeather()
  },
  methods: {
    getWeather: async function () {
      const response = await axios.get('/api/weather')
      this.tableData = response.data
      console.log(this.tableData)
    }
  },
  computed: {
    limitCount(){
      return this.tableData.slice(0, this.tableData.length)
    },
    // get_file_path: function() {
    //   return function(file_name){
    //     console.log('../../assets/laundry/0'+ file_name + '.png')
    //     return '../../assets/laundry/01.png'
    //   }
    // }
  }
}
</script>

<style scoped>
table {
  display: block;
  overflow-x: scroll;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}
figure{text-align:center;}
figcaption{font:10px arial;}
</style>